## Setup Quarto static site + GitHub Pages

**What this does**
- Adds a Quarto website (`_quarto.yml`, `index.qmd`, `about.qmd`, `styles.scss`).
- Creates `posts/` and `resources/` for content.
- Adds GitHub Action to render and publish to `gh-pages` on each push to `main`.

**After merging**
1. Go to **Settings → Pages** and choose **Deploy from a branch** → `gh-pages` (root).  
2. Push content to `posts/` and `resources/` — the site auto-updates.

**Notes**
- Theme: Bootswatch *Flatly* with a lightweight brand SCSS overlay.
- No API keys or paid services required.
