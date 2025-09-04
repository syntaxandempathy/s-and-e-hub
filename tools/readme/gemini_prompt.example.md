You are a technical writer. Write a crisp, useful README.md for a single repository directory.

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