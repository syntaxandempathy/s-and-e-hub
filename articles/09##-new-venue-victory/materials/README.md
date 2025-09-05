# Materials for AI vs. Human Writing Analysis

*Supporting documents and analysis artifacts for comparing AI-generated and human-written text.*

## Overview
This directory contains data, scripts, and analysis results related to a research project comparing AI-generated and human-written text.  The analysis focuses on identifying patterns in writing style, semantic similarity, and modification intensity across different versions of articles.  The Jupyter Notebooks document the data processing and analysis workflows. JSON files store intermediate and final results.  Markdown files contain transcripts and build notes.

## Contents
- `ai-vs-human.ipynb` — Primary Jupyter Notebook for AI vs. human writing analysis.
- `ai-vs-human-v0.1.ipynb`, `ai-vs-human-v0.2.ipynb`, `ai-vs-human-v0.3.ipynb` — Earlier versions of the main analysis notebook.
- `Claude-Python NLP Research in Colab.md` —  Research notes on using Python and Claude for NLP tasks in Google Colab.
- `0614-transcript-2.md`, `0614-transcript-3.md` — Transcripts of development sessions.
- `best-build-notes.md` — Notes on the best-performing build of the analysis pipeline.
- `markup-languages_checkpoint_steps_1_2.json`, `markup-languages_complete_analysis.json`, `markup-languages_footer_metrics.json` — JSON files containing intermediate and final analysis results for a sample article.


## Quick Start
The analysis is performed using Jupyter Notebooks.  To reproduce the results, ensure you have the necessary Python libraries installed (refer to the notebooks for details).  Open `ai-vs-human.ipynb` in a Jupyter environment and execute the cells sequentially.

## Conventions
Jupyter Notebooks are versioned using sequential numbers (v0.1, v0.2, etc.). JSON files follow a naming convention indicating the article and analysis stage.

---
Last updated: 2025-09-05
