# Syntax & Empathy — Quarto Site Ops Guide

> **TL;DR**  
> - **Source lives on `main`.** Quarto inputs (`.qmd`, `.md`, `.ipynb`) and site config are committed to `main`.  
> - **CI builds to `gh-pages`.** GitHub Actions renders the site and publishes the output HTML to the `gh-pages` branch.  
> - **Live URL:** https://syntaxandempathy.github.io/syntax-and-empathy/  
> - **Publish trigger:** any push to `main` (or manual *Run workflow*).

---

## 1) Repository layout (expected)
```
.
├─ _quarto.yml                # site config (theme, nav, render, resources)
├─ index.qmd                  # homepage
├─ about.qmd                  # about page
├─ articles/                  # your content (can have subfolders)
│  ├─ index.qmd               # section landing + listing
│  └─ ....{qmd,md,ipynb}
├─ resources/                 # PDFs/images/attachments (optional index.qmd)
├─ styles.scss                # brand variables/overrides
└─ .github/workflows/publish-quarto.yml
```

**Notes**
- Content **does not** need to be only `.qmd`; plain **`.md`** and **`.ipynb`** render too.
- If you previously had raw `.html` files, keep them as **assets** and link to them (or port to `.md`/`.qmd` if you want them themed and listed).

---

## 2) Branch strategy & where to run commands
- **Authoring:** create a feature branch (`feat/article-x`), edit content, open a PR into `main`.  
- **Publishing:** the workflow runs **on `main`** and pushes the built site to **`gh-pages`**.  
- **Do not commit to `gh-pages`** manually—CI owns it.  
- **Local preview commands** (below) run from **your feature branch at repo root**.

Optional: You *can* manually run the workflow from a branch via **Actions → Run workflow** for a smoke test, but the recommended flow is PR → merge → auto-publish from `main`.

---

## 3) Local workflow (with `uv`)
Run these at the **repo root**:

```bash
# one-time per machine (if needed)
uv venv
uv sync                                # installs deps from pyproject/uv.lock
export QUARTO_PYTHON="$PWD/.venv/bin/python"    # Windows PowerShell: $env:QUARTO_PYTHON="$PWD\.venv\Scripts\python.exe"

# preview the site locally
quarto preview

# optional: build once, clean cache
quarto render --clean
```

**Why `QUARTO_PYTHON`?** Ensures any `{python}` chunks execute using your locked `.venv` from `uv`.  
If you don’t execute code in pages, you can skip the Python bits entirely.

---

## 4) Content conventions

### 4.1 Articles directory
- Use **`articles/**`** for content; subfolders are fine.  
- Either omit `project.render` (Quarto renders all inputs) **or** include a recursive, multi-extension glob:

```yaml
project:
  type: website
  render:
    - index.qmd
    - about.qmd
    - articles/**.{qmd,md,ipynb}
```

### 4.2 Section landing & listings
Create `articles/index.qmd`:

```yaml
---
title: Articles
listing:
  contents: articles
  sort: "date desc"
  categories: true
---
```

### 4.3 Front matter for articles
At minimum:
```yaml
---
title: "Your title"
date: 2025-09-12
# categories: [design, ai]
# description: "Optional SEO summary"
# draft: true   # keep out of publish until ready
---
```

### 4.4 Assets & raw files
- Put images next to the article or under `resources/`.
- To force-copy non-rendered assets to the site output, declare them:

```yaml
project:
  resources:
    - resources/**
    - articles/**/*.pdf
    - articles/**/*.html
```

---

## 5) CI/CD (GitHub Actions)

### 5.1 What the workflow does
- Installs Quarto  
- Sets up `uv`, creates/uses `.venv` from `uv.lock`  
- Exports `QUARTO_PYTHON` so notebook/py chunks run in that env  
- Renders the site and publishes to `gh-pages`

### 5.2 Permissions & Pages
- Repo **Settings → Actions → General → Workflow permissions → Read and write**.  
- After the first successful run: **Settings → Pages → Deploy from a branch → `gh-pages` / root**.  
- `GITHUB_TOKEN` is auto-provisioned; no secret to add.

---

## 6) Common tasks

**Add a new article**
```bash
git switch -c feat/new-article
mkdir -p articles/guides
$EDITOR articles/guides/getting-started.md
# add front matter (title/date)
quarto preview
git add -A && git commit -m "Add: getting started article"
git push && open PR
```

**Rename `posts/` → `articles/`**
- Rename the folder, update navbar and any `render:`/`listing:` paths to `articles/`.  
- Rebuild: `quarto render --clean`.

**Set the live URL (canonical links & sitemap)**
```yaml
website:
  site-url: "https://syntaxandempathy.github.io/syntax-and-empathy/"
```

---

## 7) Troubleshooting

- **Index shows, subpages don’t:** your `render:` filter is too narrow. Remove it or use `articles/**.{qmd,md,ipynb}`.  
- **Action says “0 input files”:** same as above or files lack supported extensions.  
- **“Unable to locate R”:** safe to ignore unless you use `{r}` chunks.  
- **404 at live URL:** verify `Settings → Pages` is set to `gh-pages` / root and the `gh-pages` branch contains an `index.html` at the top level.  
- **Notebook/python execution errors:** ensure `uv sync` ran and `QUARTO_PYTHON` is set in CI (the provided workflow does this).

---

## 8) Policy reminders
- Treat `gh-pages` as **machine-managed**—don’t push there manually.  
- Keep **all Quarto inputs and content on `main`** (via PRs).  
- Prefer `.md`/`.qmd` for theme-consistent pages; keep raw `.html` as assets if needed.

---

**Questions or changes?**  
Edit `_quarto.yml` (nav, theme, resources), commit to a branch, open a PR, and the site will republish after merge.
