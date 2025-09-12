# 09##-Crash-Course-Collaboration: AI-Assisted Article Writing

*A documented journey of refining an AI-assisted writing process, from initial drafts to final publication.*

## Overview
This directory contains the source files and analysis results for an article detailing the iterative development of an AI-assisted writing process.  The project involved multiple drafts, refinements, and an enhanced Python analyzer (`0610-ai-writing-analyzer-enhanced.py`) to quantify changes between each revision. The analysis includes metrics such as word count, sentence length, and semantic similarity, providing insights into the collaborative process.  The final article (`04-final-article.md`) documents the entire journey, highlighting both the challenges and successes. The `materials` directory holds input and output data from the analysis.


## Contents
- `01-draft-article.md` — Initial draft of the article documenting the project.
- `02-refined-article.md` — Second draft reflecting early improvements.
- `03-edited-article.md` — Third draft after significant revisions.
- `04-final-article.md` — Final version of the article.
- `materials/code/0610-ai-writing-analyzer-enhanced.py` — Python script used to analyze the article's revisions.
- `materials/code/output/ChatGPT-Article version analysis.md` — ChatGPT analysis of the article's versions.
- `materials/code/output/markup-languages-analysis-report.md` — Analysis report for the article's markup languages.
- `materials/code/output/markup-languages-stage-metrics.csv` — CSV file with stage-level metrics.
- `materials/code/output/markup-languages-transition-analysis.csv` — CSV file with transition analysis data.
- `materials/input/*` — Input data files used for the analysis.
- `raw/00-brief.md` — Initial brief for the article.
- `raw/00-rough.md` — Rough notes and ideas for the article.


## Quick Start
The Python script `materials/code/0610-ai-writing-analyzer-enhanced.py` requires several input files (located in the `materials/input` directory).  It generates CSV output files containing metrics and transition analysis data.  Refer to the script's comments for details on input/output file paths.

## Conventions
The naming convention for article drafts follows a chronological order (e.g., `01-draft-article.md`, `02-refined-article.md`).  The `materials` directory is structured into `input` (source data) and `code/output` (analysis results).


---
Last updated: 2025-09-05
