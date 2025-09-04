README Sync (Gemini-Direct)

Automatically generates or refreshes README.md files in each directory of your repo using Google Gemini. No front matter files—Gemini writes the entire README based on the directory’s files and brief excerpts.
	•	On push to main: updates READMEs for directories touched by the push and any directory whose README is stale (older than the newest file inside that directory).
	•	Manual runs: choose full (entire repo) or target (single directory).

Paths
	•	Script: tools/readme/readme_sync.py
	•	Optional prompt override: tools/readme/gemini_prompt.md
	•	Workflow: .github/workflows/readme-sync.yml

⸻

How it works
	1.	Directory selection
	•	Changed: uses the GitHub-provided diff (before..sha) to find directories touched by the push.
	•	Stale: includes any directory where README.md is missing or older than the newest file in that directory.
	2.	Context gathering (safe & small)
	•	For each selected directory, the script collects filenames and short excerpts from text-like files (large/binary files are skipped).
	3.	Gemini prompt & generation
	•	The script builds a prompt (from a default template or your custom gemini_prompt.md) and asks Gemini to write the full README.md.
	•	If Gemini returns fenced code blocks, the script strips the fences.
	4.	Commit & push
	•	Changes are committed by github-actions[bot] and pushed back to the repository.

⸻

Requirements
	•	GitHub Actions secret: GEMINI_API_KEY
	•	Workflow runner: Ubuntu, Python 3.11
	•	Python packages: requests (installed by the workflow)

No other dependencies, no front matter (meta.yml) required.

⸻

Install
	1.	Ensure these files are in your repo:

tools/readme/readme_sync.py
tools/readme/gemini_prompt.example.md   # starter prompt (optional)
.github/workflows/readme-sync.yml


	2.	In your repo, go to Settings → Secrets and variables → Actions, add:
	•	GEMINI_API_KEY → your Google Generative Language API key
	3.	Commit to main. The workflow runs automatically on pushes.

⸻

Usage

Automatic (on push to main)
	•	The workflow invokes the script in auto mode:
	•	Changed dirs from the push range
	•	Plus stale dirs (README missing or older than contents)

Manual (Actions → “README Sync (Gemini Direct)” → “Run workflow”)
	•	mode:
	•	full — process every directory (excluding standard ignores)
	•	target — process one directory
	•	target_dir:
	•	Path relative to repo root (required if mode=target)
	•	dry_run:
	•	If true, print what would happen without writing files

The workflow will commit and push any generated changes.

⸻

Customizing the README style

Create tools/readme/gemini_prompt.md to override the default prompt. Use the placeholders below:
	•	{{DIR_NAME}} — directory name only
	•	{{TODAY}} — UTC date YYYY-MM-DD
	•	{{FILES_JSON}} — compact JSON with filenames, sizes, and short excerpts

Starter template

Save this as tools/readme/gemini_prompt.md to take effect:

You are a technical writer. Write a crisp, useful README.md for a single repository directory.

## Inputs
- Directory name: {{DIR_NAME}}
- Today: {{TODAY}}
- Files metadata (JSON): {{FILES_JSON}}

## Requirements
- Use GitHub-flavored Markdown (no HTML).
- Start with a single H1 that is a human-friendly title.
- Follow immediately with a one-sentence tagline in *italic*.
- Add an **Overview** (what this directory contains and how it’s used).
- Include a **Contents** section listing the most relevant files with one-line descriptions; use backticks for filenames.
- If scripts/configs exist, add a **Quick Start** or **Usage** section with 1–3 minimal examples.
- Add a **Conventions** or **Structure** section if helpful.
- End with a **Changelog** line: `Last updated: {{TODAY}}`.
- Do not invent external URLs. If unknown, omit links.
- Keep it clear and concise; prefer bullets where helpful.

## Output
Return only the final Markdown for README.md (no extra commentary).


⸻

Behavior details
	•	Stale detection: If README.md doesn’t exist, or its mtime is older than the newest file in the directory, it’s considered stale and will be regenerated.
	•	Exclusions: Common junk/infra dirs are ignored: .git, .github, __pycache__, node_modules, .venv, venv, .pytest_cache.
	•	Large/binary files: Skipped or summarized to keep the prompt small (e.g., images, archives, videos, >~800 KB).
	•	Idempotent: Unchanged directories are skipped; re-runs are safe.
	•	Errors: If a directory fails to generate, the job continues and logs the issue.

⸻

Troubleshooting
	•	“GEMINI_API_KEY not set.”
Add the secret under Settings → Secrets and variables → Actions. Name must be exactly GEMINI_API_KEY.
	•	Gemini error (HTTP code)
	•	Verify the key is valid and has model access.
	•	Try a simpler prompt (remove custom gemini_prompt.md to use the default).
	•	Reduce directory size or exclude unusually large text files.
	•	Nothing updates on push
	•	Ensure you’re pushing to main (or adjust the workflow branch filter).
	•	Confirm that files actually changed in a directory.
	•	Check Action logs to see which directories were selected.
	•	Manual run shows no work
	•	mode=target requires a valid target_dir.
	•	For full, ensure there are directories beyond the repo root and not excluded.

⸻

FAQ

Q: Why not store front matter?
A: You asked for the simplest flow—Gemini writes the entire README. No YAML, fewer moving parts.

Q: Can I change the voice or sections?
A: Yes. Create tools/readme/gemini_prompt.md and define the exact structure and tone you want.

Q: Does it touch files outside READMEs?
A: No. It only writes README.md files in directories it processes.

Q: Can I run it locally?
A: Yes. With Python 3.9+ and requests installed, set GEMINI_API_KEY in your environment and run:

python tools/readme/readme_sync.py --mode full
# or
python tools/readme/readme_sync.py --mode target --target-dir path/to/dir


⸻

Security & cost notes
	•	Only compact excerpts of text files are sent to Gemini (no large binaries).
	•	Keep your API key in GitHub Secrets.
	•	If cost control is important, you can:
	•	narrow manual runs to target,
	•	tweak the script limits (max files, excerpt size),
	•	or temporarily disable the Action.

⸻

License / Ownership

Generated content is committed to your repo. Review PRs as usual if you prefer to run the workflow on branches instead of pushing directly to main.

⸻

If you want this README bundled into your ZIP package as tools/readme/README.md, say the word and I’ll include it alongside the script and workflow.