# README Sync – Install

This package contains the simplified README sync implementation.

## Files

- `tools/readme/readme_sync.py` – the Python script that discovers target folders, optionally calls Gemini to write `meta.yml`, and generates `README.md`.
- `.github/workflows/readme-sync.yml` – the GitHub Actions workflow that runs the script on push or on-demand.

## Setup

1. Copy **tools/readme/readme_sync.py** into your repo at the same path.
2. Copy **.github/workflows/readme-sync.yml** into your repo at the same path.
3. In your repo settings → **Secrets and variables → Actions**, set `GEMINI_API_KEY` if you want AI enrichment (optional).
4. Push to `main` or run manually from **Actions → README Sync → Run workflow**.

## Notes

- Modes: `auto` (default), `full`, `stale`, `target`.
- For `target`, fill the `target_dir` input when triggering manually.
- The job will commit and push any changes it makes (`README.md` / `meta.yml`).

