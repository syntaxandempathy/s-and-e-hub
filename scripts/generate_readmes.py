# scripts/generate_readmes.py
from __future__ import annotations
import argparse, os, sys, fnmatch, pathlib, yaml
from datetime import date
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
TEMPLATE_MAP_FILE = TEMPLATES_DIR / "templates_map.yml"

README = "README.md"
META = "meta.yml"

EXCLUDE_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache"}

def load_templates_map() -> Dict:
    if TEMPLATE_MAP_FILE.exists():
        return yaml.safe_load(TEMPLATE_MAP_FILE.read_text(encoding="utf-8")) or {}
    return {}

def choose_template(dirpath: pathlib.Path, tmap: Dict) -> str:
    routing = (tmap.get("routing") or {})
    # compute the path of this directory relative to the repo root
    rel = str(dirpath.relative_to(ROOT)) or "."

    # 1) exact match on relative path (e.g., "." or "articles")
    if rel in routing:
        return routing[rel]

    # 2) pattern match: try patterns against the relative path first,
    #    then against the leaf directory name for backwards compatibility
    for pat, tmpl in routing.items():
        if pat in {".", "*"}:
            continue
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(dirpath.name, pat):
            return tmpl

    # 3) fallback
    return routing.get("*", "folder.md.j2")

def git_changed_dirs() -> List[pathlib.Path]:
    # base is previous commit on this branch; fallback to HEAD~1
    import subprocess
    try:
        base = subprocess.check_output(["git", "merge-base", "HEAD", "HEAD~1"]).decode().strip()
    except Exception:
        base = "HEAD~1"
    diff = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"]).decode().splitlines()
    dirs = { (ROOT / p).parent for p in diff if p.strip() }
    return sorted({d for d in dirs if d.exists()})

def iter_dirs(start: pathlib.Path) -> List[pathlib.Path]:
    out = []
    for d, subdirs, files in os.walk(start):
        dpath = pathlib.Path(d)
        if any(seg in EXCLUDE_DIRS for seg in dpath.parts):
            continue
        out.append(dpath)
    return out

def read_meta(d: pathlib.Path) -> Dict:
    m = d / META
    if m.exists():
        try:
            return yaml.safe_load(m.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}

def detect_children(d: pathlib.Path) -> List[Dict]:
    children = []
    for p in sorted(d.iterdir()):
        if p.name.startswith(".") or p.name in EXCLUDE_DIRS:
            continue
        entry = {"name": p.name, "relpath": str(p.relative_to(d))}
        if p.is_dir():
            meta = read_meta(p)
            entry.update({
                "type": "dir",
                "dir_name": p.name,
                "title": meta.get("title"),
                "tldr": (meta.get("tldr") or [None])[0],
                "has_notebook": any(x.suffix == ".ipynb" for x in p.rglob("*.ipynb")),
                "has_scripts": (p / "scripts").exists() or any(x.suffix in {".py", ".sh"} for x in p.glob("*")),
            })
        else:
            entry.update({"type": "file"})
        children.append(entry)
    return children

def newest_mtime_under(d: pathlib.Path) -> float:
    newest = 0.0
    for p in d.rglob("*"):
        if p.is_dir():
            continue
        if p.name == README:
            continue
        if any(seg in EXCLUDE_DIRS for seg in p.parts):
            continue
        try:
            newest = max(newest, p.stat().st_mtime)
        except FileNotFoundError:
            pass
    return newest

def render_for_dir(d: pathlib.Path, env: Environment, tmap: Dict) -> str:
    meta = read_meta(d)
    template_name = choose_template(d, tmap)
    print(f"[ROUTE] {d.relative_to(ROOT)} -> {template_name}")
    tmpl = env.get_template(template_name)

    # Safe metadata & feature flags for this directory
    tldr_list = meta.get("tldr") or []
    has_notebook = any(x.suffix == ".ipynb" for x in d.rglob("*.ipynb"))
    has_scripts = (d / "scripts").exists() or any(x.suffix in {".py", ".sh"} for x in d.glob("*"))
    has_critiques = (d / "critiques").exists() or any("critique" in x.name.lower() for x in d.rglob("*.md"))

    ctx = {
        "repo_name": ROOT.name,
        "dir_name": d.name,
        "dir_title": meta.get("title"),
        "title": meta.get("title"),
        "tagline": meta.get("tagline"),
        "link": meta.get("link"),
        "tldr": tldr_list,                 # safe list
        "synopsis": meta.get("synopsis"),
        "concepts": meta.get("concepts"),
        "notes": meta.get("notes"),
        "children": detect_children(d),
        "has_notebook": has_notebook,
        "has_scripts": has_scripts,
        "has_critiques": has_critiques,
        "today": date.today().isoformat(),
    }
    return tmpl.render(**ctx).rstrip() + "\n"

def write_if_needed(d: pathlib.Path, content: str, dry_run: bool) -> bool:
    out = d / README
    current = out.read_text(encoding="utf-8") if out.exists() else None
    if current != content:
        print(f"[WRITE] {out.relative_to(ROOT)}")
        if not dry_run:
            out.write_text(content, encoding="utf-8")
        return True
    print(f"[SKIP]  {out.relative_to(ROOT)} (no change)")
    return False

def collect_dirs_for_mode(mode: str, target_dir: str) -> List[pathlib.Path]:
    if mode == "auto":
        dirs = git_changed_dirs()
        return dirs or [ROOT]
    elif mode == "full":
        return iter_dirs(ROOT)
    elif mode == "stale":
        dirs = []
        for d in iter_dirs(ROOT):
            if any(seg in EXCLUDE_DIRS for seg in d.parts):
                continue
            newest = newest_mtime_under(d)
            r = d / README
            r_mtime = r.stat().st_mtime if r.exists() else 0.0
            if newest > r_mtime:
                dirs.append(d)
        return dirs
    elif mode == "target":
        base = (ROOT / target_dir).resolve()
        if not base.exists():
            print(f"Target not found: {base}")
            return []
        return iter_dirs(base)
    else:
        print(f"Unknown mode: {mode}")
        return []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="auto", choices=["auto","full","stale","target"])
    ap.add_argument("--target-dir", default="")
    ap.add_argument("--dry-run", default="false", choices=["true","false"])
    ap.add_argument("--full-rewrite-enabled", default="false", choices=["true","false"])
    args = ap.parse_args()

    if args.mode == "full" and args.full_rewrite_enabled != "true":
        print("Full rewrite blocked (enable with --full-rewrite-enabled=true).")
        sys.exit(0)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    tmap = load_templates_map()

    dirs = collect_dirs_for_mode(args.mode, args.target_dir)
    if "." in (tmap.get("routing") or {}):
        root_dir = ROOT
        if root_dir not in dirs:
            dirs.insert(0, root_dir)

    wrote_any = False
    for d in dirs:
        if any(seg in EXCLUDE_DIRS for seg in d.parts):
            continue
        content = render_for_dir(d, env, tmap)
        changed = write_if_needed(d, content, dry_run=(args.dry_run == "true"))
        wrote_any = wrote_any or changed

    if not wrote_any:
        print("No README changes were necessary.")

if __name__ == "__main__":
    main()