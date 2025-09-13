# Quarto site (GitHub Pages)

**How to enable Pages**  
1) Merge this PR.  
2) In *Settings → Pages*: set **Source:** "Deploy from a branch"; **Branch:** `gh-pages` / `/` (root).  
3) Push to `main` and the site will publish automatically.

**Local preview (optional)**  
- Install Quarto: https://quarto.org/docs/get-started/  
- Preview: `quarto preview`

**Add content**  
- Posts: add `.qmd` or `.md` under `posts/` with YAML front matter (`title`, `date`).  
- Assets: put PDF/images/etc. under `resources/` and link to them.
