#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import textwrap
from typing import Iterable, List, Dict, Any, Optional

import requests

API_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)
DEFAULT_MODEL = "gemini-1.5-flash"  # fast, low-cost
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]  # tools/readme/ -> repo root
PROMPT_PATH = REPO_ROOT / "tools" / "readme" / "gemini_prompt.md"
TEMPLATE_PATH = REPO_ROOT / "tools" / "readme" / "readme.template.md"

IGNORE_DIRS = {
    ".git", ".github", ".venv", "_site", ".quarto", "node_modules", "__pycache__",
}
README_NAME = "README.md"


def log(msg: str) -> None:
    print(msg, flush=True)


def run(cmd: List[str], cwd: Optional[pathlib.Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git_changed_files(before: Optional[str], after: Optional[str]) -> List[pathlib.Path]:
    """
    Return paths changed between two SHAs. If unavailable, return empty (caller can fall back).
    """
    if not before or not after:
        return []
    cp = run(["git", "diff", "--name-only", before, after], cwd=REPO_ROOT)
    if cp.returncode != 0:
        return []
    files = [REPO_ROOT / p for p in cp.stdout.strip().splitlines() if p.strip()]
    return [p for p in files if p.exists()]


def all_directories(root: pathlib.Path) -> List[pathlib.Path]:
    dirs = []
    for p in root.rglob("*"):
        if p.is_dir():
            rel = p.relative_to(root)
            parts = set(rel.parts)
            if parts & IGNORE_DIRS:
                continue
            dirs.append(p)
    return dirs


def is_renderable_file(p: pathlib.Path) -> bool:
    # Files worth describing; skip huge binaries by extension
    exts_keep = {".qmd", ".md", ".ipynb", ".py", ".yaml", ".yml", ".json", ".toml", ".sh", ".cfg", ".ini", ".txt"}
    exts_skip = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".zip", ".gz", ".tar", ".woff2"}
    if p.suffix.lower() in exts_skip:
        return False
    return p.suffix.lower() in exts_keep


def newest_mtime(files: Iterable[pathlib.Path]) -> float:
    ts = [f.stat().st_mtime for f in files if f.exists()]
    return max(ts) if ts else 0.0


def directories_needing_readme_auto() -> List[pathlib.Path]:
    """
    AUTO mode:
      - any directory containing a changed file
      - any directory whose README.md is missing or older than its newest source file
    """
    before = os.environ.get("GITHUB_BEFORE")
    after = os.environ.get("GITHUB_SHA")
    changed = git_changed_files(before, after)

    changed_dirs = {p.parent for p in changed if p.is_file()}
    candidates = set(changed_dirs)

    for d in all_directories(REPO_ROOT):
        if any(part in IGNORE_DIRS for part in d.relative_to(REPO_ROOT).parts):
            continue
        files = [f for f in d.iterdir() if f.is_file() and f.name != README_NAME]
        if not files:
            continue
        src_files = [f for f in files if is_renderable_file(f)]
        if not src_files:
            continue
        readme = d / README_NAME
        newest = newest_mtime(src_files)
        readme_age = readme.stat().st_mtime if readme.exists() else 0.0
        if not readme.exists() or readme_age < newest:
            candidates.add(d)

    return sorted(candidates)


def directories_full() -> List[pathlib.Path]:
    dirs = []
    for d in all_directories(REPO_ROOT):
        if any(part in IGNORE_DIRS for part in d.relative_to(REPO_ROOT).parts):
            continue
        if any(f.is_file() for f in d.iterdir()):
            dirs.append(d)
    return sorted(dirs)


def directories_target(target: str) -> List[pathlib.Path]:
    p = (REPO_ROOT / target).resolve()
    if not p.exists() or not p.is_dir():
        raise SystemExit(f"--target-dir '{target}' not found or not a directory")
    return [p]


def build_files_metadata(d: pathlib.Path) -> List[Dict[str, Any]]:
    meta = []
    for f in sorted(d.iterdir()):
        if not f.is_file() or f.name == README_NAME:
            continue
        try:
            size = f.stat().st_size
        except Exception:
            size = 0
        entry = {"name": f.name, "size_bytes": size}
        if is_renderable_file(f):
            try:
                with f.open("r", encoding="utf-8", errors="ignore") as fh:
                    text = fh.read(5000)
                lines = text.count("\n") + 1
                entry["sample"] = text[:800]
                entry["lines_estimate"] = lines
            except Exception:
                pass
        meta.append(entry)
    return meta


def load_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise SystemExit(f"Required file missing: {path}")
    return path.read_text(encoding="utf-8")


def call_gemini(prompt_text: str, api_key: str, model: str = DEFAULT_MODEL, max_tokens: int = 2048) -> str:
    url = API_URL_TEMPLATE.format(model=model, key=api_key)
    payload = {
        "generationConfig": {
            "temperature": 0.6,
            "topP": 0.95,
            "maxOutputTokens": max_tokens,
        },
        "contents": [
            {"parts": [{"text": prompt_text}]}
        ],
    }
    resp = requests.post(url, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    # Parse the first candidate text
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise RuntimeError(f"Unexpected Gemini response: {json.dumps(data)[:800]}")


def synthesize_readme(dir_path: pathlib.Path, api_key: str, model: str, dry_run: bool) -> bool:
    today = dt.date.today().isoformat()
    dir_name = str(dir_path.relative_to(REPO_ROOT)) or "."
    files_meta = build_files_metadata(dir_path)
    prompt = load_text(PROMPT_PATH)
    prompt = prompt.replace("{{DIR_NAME}}", dir_name)
    prompt = prompt.replace("{{TODAY}}", today)
    prompt = prompt.replace("{{FILES_JSON}}", json.dumps(files_meta, ensure_ascii=False, indent=2))

    log(f"➡️  Generating README for '{dir_name}' with {len(files_meta)} files described...")

    md = call_gemini(prompt, api_key, model=model)

    # Normalize whitespace a bit
    md = md.strip() + "\n"

    readme_path = dir_path / README_NAME
    existing = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    changed = (existing.strip() != md.strip())

    if dry_run:
        log(f"   (dry-run) {'would write' if changed else 'no change'}: {readme_path}")
        return False

    if changed:
        readme_path.write_text(md, encoding="utf-8")
        log(f"   ✅ wrote {readme_path}")
        return True
    else:
        log(f"   ⏭️  unchanged: {readme_path}")
        return False


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate/refresh README.md files with Gemini")
    p.add_argument("--mode", choices=["auto", "full", "target"], default="auto",
                   help="auto: changed+stale dirs; full: whole repo; target: one directory")
    p.add_argument("--target-dir", default=None, help="Directory to process when mode=target")
    p.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model, e.g., gemini-1.5-flash")
    p.add_argument("--dry-run", action="store_true", help="Compute and show changes without writing files")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        log("ERROR: GEMINI_API_KEY is not set.")
        return 2

    if args.mode == "target":
        if not args.target_dir:
            log("ERROR: --target-dir is required for mode=target")
            return 2
        targets = directories_target(args.target_dir)
    elif args.mode == "full":
        targets = directories_full()
    else:
        targets = directories_needing_readme_auto()

    if not targets:
        log("No directories to process.")
        return 0

    wrote_any = False
    for d in targets:
        try:
            changed = synthesize_readme(d, api_key, model=args.model, dry_run=args.dry_run)
            wrote_any = wrote_any or changed
        except Exception as e:
            log(f"   ❌ {d}: {e}")

    return 0 if (wrote_any or args.dry_run) else 0


if __name__ == "__main__":
    sys.exit(main())
