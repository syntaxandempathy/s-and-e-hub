#!/usr/bin/env python3
"""
Lightweight meta.yml generator using Gemini.

Cost controls:
- Only processes directories that lack meta.yml unless --overwrite
- Caps # of directories per run (--max-dirs)
- Caps # of files per dir and chars per file
- Skips binaries, large files, known junk
- Uses a fingerprint file (.meta.hash) to avoid re-calling if unchanged

Requires:
- env GEMINI_API_KEY
- requests, PyYAML
"""

from __future__ import annotations
import os, sys, json, hashlib, argparse, pathlib, mimetypes, time
import yaml, requests

API_URL_TMPL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-2.5-flash"

ROOT = pathlib.Path(__file__).resolve().parents[1]
FINGERPRINT_NAME = ".meta.hash"
META_NAME = "meta.yml"

SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache", "templates", "scripts"}
SKIP_FILES = {META_NAME, FINGERPRINT_NAME, "README.md", ".DS_Store", ".gitkeep"}

TEXT_EXTS = {
    ".md", ".txt", ".py", ".ipynb", ".json", ".yaml", ".yml", ".csv", ".tsv",
    ".sh", ".cfg", ".ini"
}

def is_binary(path: pathlib.Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS:
        return False
    mt, _ = mimetypes.guess_type(path.name)
    if mt is None:
        # Fall back: read a tiny chunk and check for null bytes
        try:
            with path.open("rb") as f:
                chunk = f.read(800)
            return b"\x00" in chunk
        except Exception:
            return True
    return not mt.startswith(("text/", "application/json"))

def digest_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]

def hash_dir_snapshot(d: pathlib.Path, max_files: int, max_chars: int) -> str:
    """Create a cheap fingerprint of filenames + first N chars of small text files."""
    items = []
    count = 0
    for p in sorted(d.iterdir()):
        if p.is_dir():
            continue
        if p.name in SKIP_FILES:
            continue
        if is_binary(p):
            items.append({"name": p.name, "kind": "bin", "size": p.stat().st_size})
            continue
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            raw = ""
        head = raw[:max_chars]
        items.append({"name": p.name, "kind": "text", "head": head})
        count += 1
        if count >= max_files:
            break
    blob = json.dumps(items, sort_keys=True).encode("utf-8")
    return digest_bytes(blob)

def gather_preview(d: pathlib.Path, max_files: int, max_chars: int) -> list[dict]:
    """Small summary we send to Gemini (kept tiny)."""
    preview = []
    count = 0
    for p in sorted(d.iterdir()):
        if p.is_dir() or p.name in SKIP_FILES:
            continue
        rec = {"name": p.name, "size": p.stat().st_size}
        if not is_binary(p):
            try:
                raw = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                raw = ""
            rec["head"] = raw[:max_chars]
        else:
            rec["head"] = ""
        preview.append(rec)
        count += 1
        if count >= max_files:
            break
    return preview

def looks_like_article(preview: list[dict]) -> bool:
    names = " ".join([r["name"].lower() for r in preview])
    # rough signals: has md content; or scripts/notebooks
    return any(n.endswith(".md") for n in names.split()) or "script" in names or "notebook" in names or "colab" in names

PROMPT = """You are helping create a small YAML metadata file for a GitHub folder that is a companion to an AI/design article series.

Given a list of files (names, sizes, and short excerpts for text files), produce a compact YAML with this schema:

title: <human-friendly title inferred from folder and files>
tagline: <1 short line, audience-friendly>
tldr:
  - <what this folder is>
  - <who it's for>
  - <what you'll do or find here>
link: <leave blank if unknown>
synopsis: <one-paragraph summary, plain language>
# Optional; include only if clearly relevant:
concepts: |
  - <bullet 1>
  - <bullet 2>

Rules:
- Keep it under ~120 lines; be concise.
- If uncertainty is high, be conservative and generic.
- DO NOT fabricate links.
- Output ONLY valid YAML. No backticks, no prose.
"""

def call_gemini(api_key: str, model: str, preview: list[dict], folder_name: str) -> dict | None:
    url = API_URL_TMPL.format(model=model)
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": PROMPT},
                {"text": f"Folder name: {folder_name}"},
                {"text": "Files (JSON):\n" + json.dumps(preview, ensure_ascii=False, indent=2)}
            ]
        }]
    }
    params = {"key": api_key}
    r = requests.post(url, headers=headers, params=params, data=json.dumps(payload), timeout=60)
    if r.status_code != 200:
        print(f"[GEMINI] HTTP {r.status_code}: {r.text[:200]}")
        return None
    data = r.json()
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        print("[GEMINI] Unexpected response shape")
        return None
    try:
        meta = yaml.safe_load(text) or {}
        if not isinstance(meta, dict):
            return None
        return meta
    except Exception as e:
        print(f"[GEMINI] YAML parse error: {e}")
        return None

def should_process_dir(d: pathlib.Path, only_missing: bool) -> bool:
    if d.name.startswith(".") or d.name in SKIP_DIRS:
        return False
    if (d / META_NAME).exists() and only_missing:
        return False
    # ignore folders that truly have nothing but ignorable files
    for p in d.iterdir():
        if p.is_dir() and p.name not in SKIP_DIRS:
            return True
        if p.name not in SKIP_FILES:
            return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="articles", help="Subtree to scan")
    ap.add_argument("--only-missing", action="store_true", help="Only create meta.yml if absent")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing meta.yml")
    ap.add_argument("--max-dirs", default="3")
    ap.add_argument("--max-files-per-dir", default="6")
    ap.add_argument("--max-chars-per-file", default="1200")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", default="false", choices=["true","false"])
    args = ap.parse_args()

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        print("GEMINI_API_KEY not set; exiting.")
        sys.exit(0)

    root = (ROOT / args.root).resolve()
    if not root.exists():
        print(f"Root not found: {root}")
        sys.exit(0)

    max_dirs = int(args.max_dirs)
    max_files = int(args.max_files_per_dir)
    max_chars = int(args.max_chars_per_file)
    dry = (args.dry_run == "true")

    processed = 0
    for d, subdirs, files in os.walk(root):
        dpath = pathlib.Path(d)
        if any(seg in SKIP_DIRS for seg in dpath.parts):
            continue
        if not should_process_dir(dpath, only_missing=not args.overwrite):
            continue

        # cheap fingerprint to avoid repeat calls
        snap = hash_dir_snapshot(dpath, max_files, max_chars)
        fp_file = dpath / FINGERPRINT_NAME
        prev = fp_file.read_text(encoding="utf-8") if fp_file.exists() else ""
        if snap == prev and (dpath / META_NAME).exists():
            print(f"[SKIP] {dpath.relative_to(ROOT)} unchanged (fingerprint)")
            continue

        preview = gather_preview(dpath, max_files, max_chars)
        # If it doesn't look like an article-ish folder, still allow YAML but keep it generic
        # (we rely on README routing for final presentation).
        print(f"[AI] Generating meta for {dpath.relative_to(ROOT)} with {len(preview)} files (capped).")
        meta = call_gemini(api_key, args.model, preview, dpath.name)
        if meta is None:
            print(f"[AI] Failed to create meta for {dpath.relative_to(ROOT)}")
            continue

        # Write meta.yml
        meta_path = dpath / META_NAME
        if dry:
            print(f"[DRY] Would write: {meta_path.relative_to(ROOT)}")
        else:
            with meta_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True)
            fp_file.write_text(snap, encoding="utf-8")
            print(f"[WRITE] {meta_path.relative_to(ROOT)}")

        processed += 1
        if processed >= max_dirs:
            print(f"[STOP] Reached --max-dirs={max_dirs}")
            break

if __name__ == "__main__":
    main()