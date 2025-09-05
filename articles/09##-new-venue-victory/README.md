# 09##-new-venue-victory: Reproducible Colab Pipeline for Authorship Analysis

*A documented pipeline for analyzing human and AI contributions in article writing, built using Google Colab.*

## Overview

This directory contains the materials and data resulting from the development of a reproducible Google Colab pipeline designed to analyze the relative contributions of human writers and AI models in the creation of articles.  The pipeline processes multiple versions of an article (draft, refined, edited, final) and generates metrics showing the evolution of content across each stage.  The project overcomes previous challenges related to reproducibility and transparency using a structured Colab notebook workflow. The analysis includes word counts, similarity scores, and visualization charts. This repository documents the final iteration of the pipeline along with intermediate steps.

## Contents

* `01-draft-article.md` — First draft of the article detailing the pipeline's development.
* `02-refined-article.md` — Refined version of the article, incorporating feedback.
* `03-edited-article.md` — Final edited version of the article, ready for publication.
* `04-final-article.md` — Placeholder for the final published article (currently empty).
* `materials/0614-transcript-2.md` — Transcript of development discussion.
* `materials/0614-transcript-3.md` — Transcript of development discussion.
* `materials/Claude-Python NLP Research in Colab.md` — Detailed notes on Claude-assisted Python development in Colab.
* `materials/ai-vs-human-v0.1.ipynb` — Initial Colab notebook version.
* `materials/ai-vs-human-v0.2.ipynb` — Second Colab notebook version.
* `materials/ai-vs-human-v0.3.ipynb` — Third Colab notebook version.
* `materials/ai-vs-human.ipynb` — Final Colab notebook version.
* `materials/best-build-notes.md` — Notes summarizing successful build process and lessons learned.
* `materials/markup-languages_checkpoint_steps_1_2.json` — Checkpoint data from pipeline execution.
* `materials/markup-languages_complete_analysis.json` — Complete analysis results in JSON format.
* `materials/markup-languages_footer_metrics.json` — Summary footer metrics in JSON format.
* `raw/00-brief.md` — Initial project brief.


## Usage

The Colab notebooks (`materials/*.ipynb`) are the core components of the pipeline.  They require mounting a Google Drive to access the article versions and configuration data.  The notebooks should be executed sequentially, starting with `materials/ai-vs-human-v0.1.ipynb`.  Each notebook builds upon the previous one, culminating in a complete analysis in `materials/ai-vs-human.ipynb`.

## Conventions

The project uses a versioning scheme for Colab notebooks (e.g., `ai-vs-human-v0.1.ipynb`, `ai-vs-human-v0.2.ipynb`), reflecting iterative development. JSON files store structured data from different stages of the pipeline.  Markdown files contain the article drafts and project notes.


---
Last updated: 2025-09-05
