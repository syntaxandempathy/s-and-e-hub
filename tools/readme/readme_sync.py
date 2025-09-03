#!/usr/bin/env python3
"""
Readme Sync - single-file rewrite
- Detects changed directories on push using the GitHub-provided before..sha
- Supports modes: auto | full | stale | target
- Optional AI enrichment via Gemini to write meta.yml
- Generates a simple, consistent README.md without Jinja (no template deps)
Dependencies: Python 3.9+, pip: requests, pyyaml
"""
from __future__ import annotations
import argparse, os, sys, subprocess, json, time, re, hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Set, Dict, Optional

try:
    import yaml  # PyYAML
    import requests
except Exception:
    print("[FATAL] Missing dependencies. Please 'pip install requests pyyaml'.", file=sys.stderr)
    raise

EXCLUDES = {".git", ".github", "__pycache__", "node_modules", ".venv", "venv", ".pytest_cache"}
README_NAME = "README.md"
META_NAME = "meta.yml"
FINGERPRINT_NAME = ".meta.hash"

def sh(cmd: List[str], cwd: Optional[Path] = None, allow_fail: bool = False) -> str:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if p.returncode != 0 and not allow_fail:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()

def repo_root() -> Path:
    try:
        out = sh(["git", "rev-parse", "--show-toplevel"])
        return Path(out)
    except Exception:
        return Path.cwd()

def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & EXCLUDES)

def all_dirs(base: Path) -> List[Path]:
    out = []
    for p, dnames, fnames in os.walk(base):
        pp = Path(p)
        if is_ignored(pp.relative_to(base)):
            dnames[:] = [d for d in dnames if d not in EXCLUDES]
            continue
        out.append(pp)
    return out

def newest_mtime(dirpath: Path) -> float:
    newest = 0.0
    for root, dnames, fnames in os.walk(dirpath):
        for f in fnames:
            fp = Path(root) / f
            try:
                newest = max(newest, fp.stat().st_mtime)
            except FileNotFoundError:
                pass
    return newest

def git_changed_dirs(base: Path, rng: Optional[str]) -> Set[Path]:
    if not rng:
        rng = "HEAD^..HEAD"
    try:
        out = sh(["git", "diff", "--name-only", rng], cwd=base, allow_fail=False)
    except RuntimeError:
        out = sh(["git", "ls-files"], cwd=base, allow_fail=True)
    dirs: Set[Path] = set()
    for line in out.splitlines():
        if not line.strip():
            continue
        p = (base / line.strip()).resolve()
        if not p.exists():
            parent = (base / Path(line.strip()).parent).resolve()
        else:
            parent = p.parent
        try:
            rel = parent.relative_to(base)
        except Exception:
            continue
        if not is_ignored(rel):
            dirs.add(parent)
            if parent.parent != base and not is_ignored(parent.parent.relative_to(base)):
                dirs.add(parent.parent)
    return dirs

def discover_candidates(base: Path, mode: str, target_dir: str, stale_days: int, changed_range: Optional[str]) -> List[Path]:
    if mode == "target":
        if not target_dir:
            print("[ERROR] mode=target requires --target-dir", file=sys.stderr)
            sys.exit(2)
        td = (base / target_dir).resolve()
        if not td.exists() or not td.is_dir():
            print(f"[ERROR] target directory not found: {td}", file=sys.stderr)
            sys.exit(2)
        return [td]
    if mode == "full":
        return [d for d in all_dirs(base) if d != base and not is_ignored(d.relative_to(base))]
    if mode == "stale":
        cands = []
        for d in all_dirs(base):
            if d == base or is_ignored(d.relative_to(base)):
                continue
            readme = d / README_NAME
            if readme.exists():
                if newest_mtime(d) > readme.stat().st_mtime + 1:
                    cands.append(d)
            else:
                cands.append(d)
        return cands
    # auto
    dirs = git_changed_dirs(base, changed_range)
    extra = []
    for d in list(dirs):
        for child in d.iterdir() if d.exists() else []:
            if child.is_dir() and (child / README_NAME).exists() is False and not is_ignored(child.relative_to(base)):
                extra.append(child)
    return sorted(set(list(dirs) + extra))

def load_yaml(path: Path) -> Dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def dump_yaml(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def short_excerpt(fp: Path, max_chars: int = 600) -> str:
    try:
        text = fp.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]

def fingerprint_for_dir(d: Path, max_files: int = 32, max_chars_per_file: int = 1000) -> str:
    h = hashlib.sha256()
    files = []
    for root, dnames, fnames in os.walk(d):
        for name in sorted(fnames):
            fp = Path(root) / name
            try:
                if fp.stat().st_size > 512_000:
                    continue
            except FileNotFoundError:
                continue
            if any(name.endswith(ext) for ext in (".png",".jpg",".jpeg",".gif",".webp",".pdf",".bin",".exe",".zip",".tar",".gz",".mp4",".mov",".wav",".ogg",".mp3",".ipynb_checkpoints")):
                continue
            files.append(fp)
            if len(files) >= max_files:
                break
        if len(files) >= max_files:
            break
    for fp in files:
        h.update(fp.name.encode())
        h.update(str(fp.stat().st_size).encode())
        h.update(short_excerpt(fp, max_chars_per_file).encode())
    return h.hexdigest()

def gemini_generate_meta(d: Path, api_key: str, model: str, overwrite: bool, debug: bool=False) -> Dict:
    meta_path = d / META_NAME
    fp_path = d / FINGERPRINT_NAME
    if meta_path.exists() and not overwrite:
        if debug: print(f"[AI] Skip (meta exists): {d}")
        return load_yaml(meta_path)
    fp_new = fingerprint_for_dir(d)
    if fp_path.exists():
        try:
            old = fp_path.read_text().strip()
            if old == fp_new and meta_path.exists() and not overwrite:
                if debug: print(f"[AI] Skip (unchanged contents): {d}")
                return load_yaml(meta_path)
        except Exception:
            pass
    files_list = []
    for root, dnames, fnames in os.walk(d):
        for name in sorted(fnames):
            p = Path(root)/name
            try:
                sz = p.stat().st_size
            except FileNotFoundError:
                continue
            if sz > 512_000:
                continue
            ext = p.suffix.lower()
            if ext in {".png",".jpg",".jpeg",".gif",".webp",".pdf",".bin",".exe",".zip",".tar",".gz",".mp4",".mov",".wav",".ogg",".mp3"}:
                continue
            files_list.append({"path": str(p.relative_to(d)), "size": sz, "excerpt": short_excerpt(p, 800)})
        if len(files_list) > 40:
            break
    prompt = {
        "role": "user",
        "parts": [{
            "text": (
                "Create a concise YAML metadata file with keys: "
                "title, tagline, tldr (3 bullet items), link, synopsis, tags (3-7), audience, updated (YYYY-MM-DD).\n"
                f"Folder name: {d.name}\n"
                "Files with small excerpts follow as JSON. Infer a human-friendly title and synopsis from them. "
                "If link is unknown, leave it empty. Today's date is {}.\n\n"
                "{}"
            ).format(datetime.utcnow().date().isoformat(), json.dumps(files_list)[:18000])
        }]
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    try:
        r = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps({"contents":[prompt]}), timeout=60)
        if r.status_code != 200:
            print(f"[AI] Gemini error {r.status_code}: {r.text[:200]}", file=sys.stderr)
            return load_yaml(meta_path) if meta_path.exists() else {}
        data = r.json()
        text = ""
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass
        if not text:
            print("[AI] No text returned from Gemini.", file=sys.stderr)
            return load_yaml(meta_path) if meta_path.exists() else {}
        m = re.search(r"```(?:yaml|yml)?\s*(.*?)```", text, re.S|re.I)
        if m:
            text = m.group(1).strip()
        try:
            meta = yaml.safe_load(text) or {}
            if not isinstance(meta, dict):
                meta = {}
        except Exception:
            meta = {"title": d.name, "synopsis": text.strip()[:1000]}
        meta.setdefault("updated", datetime.utcnow().date().isoformat())
        dump_yaml(meta_path, meta)
        fp_path.write_text(fp_new)
        return meta
    except requests.RequestException as e:
        print(f"[AI] Request failed: {e}", file=sys.stderr)
        return load_yaml(meta_path) if meta_path.exists() else {}

def ensure_meta(d: Path, args) -> Dict:
    meta_path = d / META_NAME
    meta = load_yaml(meta_path)
    if args.ai_enrich:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            print("[AI] GEMINI_API_KEY not set; skipping enrichment.")
        else:
            meta = gemini_generate_meta(d, api_key, args.gemini_model, overwrite=args.overwrite_meta, debug=args.debug)
    meta.setdefault("title", d.name.replace("-", " ").title())
    meta.setdefault("tagline", "")
    meta.setdefault("tldr", [])
    meta.setdefault("link", "")
    meta.setdefault("synopsis", "")
    meta.setdefault("tags", [])
    meta.setdefault("audience", "")
    meta.setdefault("updated", datetime.utcnow().date().isoformat())
    if not (d / META_NAME).exists() and not args.dry_run:
        dump_yaml(d / META_NAME, meta)
    return meta

def render_readme(d: Path, meta: Dict) -> str:
    lines = []
    title = meta.get("title") or d.name
    lines.append(f"# {title}\n")
    if meta.get("tagline"):
        lines.append(f"_{meta['tagline']}_\n")
    if meta.get("synopsis"):
        lines.append(f"\n{meta['synopsis']}\n")
    if meta.get("tldr"):
        lines.append("\n**TL;DR**")
        for item in meta["tldr"][:6]:
            lines.append(f"- {item}")
    if meta.get("link"):
        lines.append(f"\n**Article / Project link:** {meta['link']}")
    lines.append("\n---\n")
    lines.append("## Files")
    for root, dnames, fnames in os.walk(d):
        rootp = Path(root)
        rel = rootp.relative_to(d)
        if str(rel) != ".":
            lines.append(f"\n### {rel}")
        for name in sorted(fnames):
            if name == README_NAME or name == META_NAME or name == FINGERPRINT_NAME:
                continue
            p = rootp / name
            rp = p.relative_to(d)
            lines.append(f"- `{rp.as_posix()}`")
    updated = meta.get("updated") or datetime.utcnow().date().isoformat()
    lines.append("\n---\n")
    lines.append(f"_Auto-generated on {updated}_")
    return "\n".join(lines) + "\n"

def write_readme(d: Path, content: str, dry_run: bool) -> bool:
    out = d / README_NAME
    if dry_run:
        print(f"[DRY] Would write {out}")
        return False
    out.write_text(content, encoding="utf-8")
    return True

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Readme Sync")
    ap.add_argument("--mode", choices=["auto","full","stale","target"], default="auto")
    ap.add_argument("--target-dir", default="")
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ai-enrich", action="store_true")
    ap.add_argument("--overwrite-meta", action="store_true", help="Allow overwriting an existing meta.yml")
    ap.add_argument("--gemini-model", default="gemini-1.5-flash", help="Gemini model id")
    ap.add_argument("--debug", action="store_true")
    return ap.parse_args()

def main():
    args = parse_args()
    base = repo_root()
    changed_range = None
    before = os.environ.get("GITHUB_BEFORE", "")
    sha = os.environ.get("GITHUB_SHA", "")
    if before and sha:
        changed_range = f"{before}..{sha}"
    print(f"[INFO] repo={base}")
    print(f"[INFO] mode={args.mode} target={args.target_dir!r} dry_run={args.dry_run} ai_enrich={args.ai_enrich} overwrite_meta={args.overwrite_meta}")
    print(f"[INFO] changed_range={changed_range or 'HEAD^..HEAD'}")
    candidates = discover_candidates(base, args.mode, args.target_dir, args.stale_days, changed_range)
    if not candidates:
        print("[INFO] No candidate directories to process.")
        return 0
    print(f"[INFO] Processing {len(candidates)} directorie(s).")
    changed = 0
    for d in sorted(candidates):
        try:
            rel = d.relative_to(base)
        except Exception:
            rel = d
        if is_ignored(rel):
            continue
        meta = ensure_meta(d, args)
        content = render_readme(d, meta)
        if write_readme(d, content, args.dry_run):
            changed += 1
            print(f"[OK] Wrote {d / README_NAME}")
    print(f"[SUMMARY] dirs={len(candidates)} wrote={changed} dry_run={args.dry_run}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
