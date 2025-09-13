# Quarto Site – Command Guide (Syntax & Empathy)

**TL;DR**  
- Work on the `main` branch.  
- Push → README Sync runs (optional) → **Quarto rebuilds HTML fresh** → site publishes to `gh-pages`.  
- Local dev: `uv venv && uv sync` then `quarto preview`.

## 1) Install & Verify Quarto

```bash
quarto --version           # confirm install
quarto check               # checks engines + basic setup
quarto check jupyter       # confirm Jupyter/Python path Quarto will use
````

## 2) Local Python via uv (recommended)

```bash
uv venv                    # create .venv
uv sync                    # install deps from pyproject/uv.lock
# macOS/Linux:
export QUARTO_PYTHON="$PWD/.venv/bin/python"
# Windows PowerShell:
$env:QUARTO_PYTHON = "$PWD\.venv\Scripts\python.exe"

# (Optional) register a named kernel for .ipynb/.qmd code chunks
uv run python -m ipykernel install --user --name syntax-env --display-name "Python (.venv)"

# sanity checks
uv run python --version
uv run jupyter --version
```

> In a page that runs Python, you can pin the kernel via front matter:
> `jupyter: syntax-env`

## 3) Preview (live reload)

```bash
quarto preview                 # preview entire site at http://localhost:XXXX
quarto preview index.qmd       # preview just the homepage
quarto preview articles/       # preview a section/folder
quarto preview --port 7777     # custom port
quarto preview --no-browser    # don’t auto-open a tab
```

**Tips**
* Preview rebuilds incrementally as you edit files.
* If something gets “stale,” stop and re-run preview.

## 4) Render (build HTML to `_site/`)

```bash
quarto render                      # render the whole site
quarto render --clean              # nuke old outputs, then render fresh (CI uses this)
quarto render index.qmd            # render a single page
quarto render 'articles/**.{md,qmd,ipynb}'   # render a subset (quote the glob)
quarto render --to html            # be explicit about format (optional)
```

**When to use `--clean`**
* After changing `_quarto.yml`, theme/SCSS, or site structure.
* When a page looks inconsistent after lots of edits.

## 5) Profiles (optional, for alt configs)
Put overrides in `_quarto-<profile>.yml` (e.g., `_quarto-dev.yml`), then:

```bash
quarto render --profile dev
quarto preview --profile dev
```

Use this to flip themes, analytics, or paths without editing the main config.

## 6) Execution & caching (notebooks/code blocks)
Your site is set to:

```yaml
execute:
  freeze: auto
```

Meaning: Quarto reuses results unless the source changes.

**Useful moves**
* Force a clean rebuild of HTML: `quarto render --clean`.
* Re-run a specific page’s code: edit the page (changes bust the “freeze”), then `quarto render path/to/page.ipynb`.
* Disable code execution for one page (front matter):

  ```yaml
  execute: false
  ```
* If a page still won’t re-execute and you need a hard reset, delete its `_freeze/` artifacts for that page/folder and render again.

## 7) Publish (you normally don’t run this locally)
CI already publishes to `gh-pages` on every push to `main`.
If you *must* publish manually from your machine (rare):

```bash
quarto render --clean
quarto publish gh-pages
```

> Prefer the GitHub Action—it’s consistent and uses your pinned toolchain.

## 8) Content scope & assets
Your `_quarto.yml` (core pieces):

```yaml
project:
  type: website
  # Either omit 'render:' to include everything, or keep it tight:
  render:
    - index.qmd
    - about.qmd
    - articles/**.{qmd,md,ipynb}
    - resources/**.{qmd,md}
  resources:
    - assets/**          # logos, icons, CSS, images
    - resources/**       # downloads / attachments

website:
  site-url: "https://syntaxandempathy.github.io/syntax-and-empathy/"
format:
  html:
    theme:
      - flatly
      - styles.scss        # brand SCSS (has Quarto theme markers)
    include-in-header:
      - _includes/fonts.html
```

**Rules of thumb**
* Make pages as `.md` (or `.ipynb`) so they inherit the theme.
* `index.md` inside a folder becomes that folder’s landing page.
* Avoid shipping raw `.html` as content—Quarto won’t style it. Keep raw HTML/PDFs under `resources/` and link to them.

## 9) Common “why does this page look off?” checks
1. The page’s path isn’t included in `project.render` → either add it or remove the `render:` block.
2. The page has a `format:` block that **overrides** site theme—remove it or include `styles.scss`.
3. `styles.scss` lost Quarto’s markers:
   * Must contain `/*-- scss:defaults --*/` and `/*-- scss:rules --*/`.
4. You forgot to rebuild clean after theme/config changes → `quarto render --clean`.
5. The page isn’t actually rendered (e.g., it’s raw HTML). Convert to `.md`/`.ipynb`.

## 10) One-liners you’ll actually use

```bash
# Start fresh preview of everything (dev loop)
uv venv && uv sync && export QUARTO_PYTHON="$PWD/.venv/bin/python" && quarto preview

# Clean rebuild after theme/config changes
quarto render --clean

# Focused rebuild of just the articles
quarto render 'articles/**.{md,qmd,ipynb}'

# Verify engines if code won’t run
quarto check jupyter
```

## 11) GitHub Pages (one-time)
* Settings → **Pages** → Deploy from a branch → **`gh-pages` / root**.
You’re done—push to `main` and the workflow handles the rest.