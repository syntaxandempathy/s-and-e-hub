# AI-Assisted Writing: A Reproducible Colab Pipeline

*A case study documenting the development of a robust pipeline for analyzing AI/human contributions in writing.*

## Overview
This directory contains the source materials and analysis results for a project aimed at creating a reproducible pipeline to measure the balance of human and AI contributions in writing.  The initial attempts, documented in `meta.yml`, highlight the challenges and lessons learned.  The final pipeline, built in Google Colab, is showcased in the `10##-new-venue-victory` subdirectory. The project uses Python and various NLP libraries for semantic analysis and similarity comparisons.  The Colab notebooks and supporting materials demonstrate a complete, reproducible workflow for analyzing articles across multiple versions.

## Contents
- `meta.yml` — Metadata about the project, including a synopsis and lessons learned.
- `10##-new-venue-victory/01-draft-article.md` — First draft of the case study article.
- `10##-new-venue-victory/02-refined-article.md` — Refined version of the article.
- `10##-new-venue-victory/03-edited-article.md` — Edited version of the article.
- `10##-new-venue-victory/04-final-article.md` — Final version of the article.
- `10##-new-venue-victory/materials/*.md` — Supporting materials, including transcripts and notes.
- `10##-new-venue-victory/materials/*.ipynb` — Google Colab notebooks detailing the analysis pipeline.
- `10##-new-venue-victory/materials/*.json` — JSON files containing analysis results and checkpoints.


## Quick Start
The analysis pipeline is implemented in Google Colab notebooks.  To run the analysis, open `10##-new-venue-victory/materials/ai-vs-human.ipynb` in Google Colab and follow the instructions in the notebook. You'll need to mount your Google Drive to access the necessary data files.


## Conventions
The project follows a version-controlled approach, tracking different stages of article development (draft, refined, edited, final).  Analysis results are stored as JSON files, providing structured data for further analysis and visualization. Google Colab notebooks are used for the main analysis pipeline and are broken into discrete, reproducible steps.


---
Last updated: 2025-09-13
