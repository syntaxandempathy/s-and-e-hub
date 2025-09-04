#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, sys, subprocess, json, re
from pathlib import Path
from datetime import datetime
from typing import List, Set, Dict, Optional
import requests

EXCLUDES = {'.git', '.github', '__pycache__', 'node_modules', '.venv', 'venv', '.pytest_cache'}
README_NAME = 'README.md'

def sh(cmd: List[str], cwd: Optional[Path] = None, allow_fail: bool = False) -> str:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if p.returncode != 0 and not allow_fail:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()

def repo_root() -> Path:
    try:
        out = sh(['git', 'rev-parse', '--show-toplevel'])
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
        rng = 'HEAD^..HEAD'
    try:
        out = sh(['git', 'diff', '--name-only', rng], cwd=base, allow_fail=False)
    except RuntimeError:
        out = sh(['git', 'ls-files'], cwd=base, allow_fail=True)
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

def discover_candidates(base: Path, mode: str, target_dir: str, changed_range: Optional[str]) -> List[Path]:
    if mode == 'target':
        if not target_dir:
            print('[ERROR] mode=target requires --target-dir', file=sys.stderr)
            sys.exit(2)
        td = (base / target_dir).resolve()
        if not td.exists() or not td.is_dir():
            print(f'[ERROR] target directory not found: {td}', file=sys.stderr)
            sys.exit(2)
        return [td]
    if mode == 'full':
        return [d for d in all_dirs(base) if d != base and not is_ignored(d.relative_to(base))]
    # auto: changed + stale
    dirs = git_changed_dirs(base, changed_range)
    for d in all_dirs(base):
        if d == base or is_ignored(d.relative_to(base)):
            continue
        readme = d / README_NAME
        if not readme.exists():
            dirs.add(d); continue
        try:
            if newest_mtime(d) > readme.stat().st_mtime + 1:
                dirs.add(d)
        except FileNotFoundError:
            dirs.add(d)
    return sorted(dirs)

def short_excerpt(fp: Path, max_chars: int = 1200) -> str:
    try:
        text = fp.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_chars]

def gather_context(d: Path, max_files: int = 60) -> Dict:
    files = []
    for root, dnames, fnames in os.walk(d):
        for name in sorted(fnames):
            p = Path(root) / name
            rel = p.relative_to(d)
            try:
                sz = p.stat().st_size
            except FileNotFoundError:
                continue
            if name == README_NAME:
                continue
            if sz > 800_000 or p.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.webp','.pdf','.bin','.exe','.zip','.tar','.gz','.mp4','.mov','.wav','.ogg','.mp3'}:
                files.append({'path': str(rel), 'size': sz, 'skipped': True})
                continue
            files.append({'path': str(rel), 'size': sz, 'excerpt': short_excerpt(p)})
            if len(files) >= max_files:
                break
        if len(files) >= max_files:
            break
    return {'dir': d.name, 'relpath': str(d), 'files': files}

def load_prompt_template(base: Path) -> str:
    custom = base / 'tools' / 'readme' / 'gemini_prompt.md'
    if custom.exists():
        try:
            return custom.read_text(encoding='utf-8')
        except Exception:
            pass
    return """You are a technical writer. Write a crisp, useful README.md for a single repository directory.

## Inputs
- Directory name: {{DIR_NAME}}
- Today: {{TODAY}}
- Files metadata (JSON): {{FILES_JSON}}

## Requirements
- Use GitHub-flavored Markdown (no HTML).
- Start with a single H1 that is a human-friendly title.
- Follow immediately with a one-sentence tagline in *italic*.
- Add an **Overview** section (3–6 sentences) explaining what the directory contains and how to use it.
- Include a **Contents** section listing the most relevant files with one-line descriptions; use backticks for filenames.
- If scripts/configs are present, add a **Quick Start** or **Usage** section with 1–3 minimal examples.
- Add a **Conventions** or **Structure** section if you detect patterns worth noting.
- End with a **Changelog** line: `Last updated: {{TODAY}}`.
- Do not invent external URLs. If unknown, omit links.
- Keep the README clear and concise (prefer bullets when helpful).

## Output
Return only the final Markdown for README.md (no extra commentary).
"""

def render_prompt(template: str, d: Path, ctx: Dict) -> str:
    content = template
    content = content.replace('{{DIR_NAME}}', d.name)
    content = content.replace('{{TODAY}}', datetime.utcnow().date().isoformat())
    fj = json.dumps(ctx['files'], ensure_ascii=False)[:18000]
    content = content.replace('{{FILES_JSON}}', fj)
    return content

def gemini_generate_readme(d: Path, api_key: str, model: str, prompt_template: str) -> str:
    prompt_text = render_prompt(prompt_template, d, gather_context(d))
    body = {'contents': [{'role': 'user', 'parts': [{'text': prompt_text}]}]}
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    r = requests.post(url, headers={'Content-Type':'application/json'}, data=json.dumps(body), timeout=90)
    if r.status_code != 200:
        raise RuntimeError(f'Gemini error {r.status_code}: {r.text[:300]}')
    data = r.json()
    text = ''
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        pass
    if not text:
        raise RuntimeError('Gemini returned no text')
    m = re.search(r"""```(?:md|markdown)?\s*(.*?)```""", text, re.S|re.I)
    if m:
        text = m.group(1).strip()
    return text.strip() + '\n'

def write_readme(d: Path, content: str, dry: bool) -> bool:
    out = d / README_NAME
    if dry:
        print(f'[DRY] Would write {out}')
        return False
    out.write_text(content, encoding='utf-8')
    return True

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description='Generate README.md with Gemini')
    ap.add_argument('--mode', choices=['full','target','auto'], default='auto')
    ap.add_argument('--target-dir', default='')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--gemini-model', default='gemini-1.5-flash', help='Gemini model id')
    return ap.parse_args()

def main():
    args = parse_args()
    base = repo_root()
    before = os.environ.get('GITHUB_BEFORE', '')
    sha = os.environ.get('GITHUB_SHA', '')
    changed_range = f'{before}..{sha}' if (before and sha) else None

    print(f'[INFO] repo={base}')
    print(f'[INFO] mode={args.mode} target={args.target_dir!r} dry_run={args.dry_run}')
    print(f'[INFO] changed_range={changed_range or "HEAD^..HEAD"}')

    if args.mode == 'full':
        candidates = discover_candidates(base, 'full', '', changed_range)
    elif args.mode == 'target':
        candidates = discover_candidates(base, 'target', args.target_dir, changed_range)
    else:
        candidates = discover_candidates(base, 'auto', '', changed_range)

    if not candidates:
        print('[INFO] No candidate directories to process.')
        return 0

    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        print('[ERROR] GEMINI_API_KEY not set.', file=sys.stderr)
        return 2

    prompt_template = load_prompt_template(base)

    wrote = 0
    for d in candidates:
        try:
            rel = d.relative_to(base)
            if is_ignored(rel):
                continue
        except Exception:
            pass

        try:
            md = gemini_generate_readme(d, api_key, args.gemini_model, prompt_template)
            if write_readme(d, md, args.dry_run):
                wrote += 1
                print(f'[OK] Wrote {d / README_NAME}')
        except Exception as e:
            print(f'[WARN] Failed to build README for {d}: {e}', file=sys.stderr)
            continue

    print(f'[SUMMARY] dirs={len(candidates)} wrote={wrote} dry_run={args.dry_run}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
