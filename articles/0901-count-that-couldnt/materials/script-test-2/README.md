# script-test-2

*A collection of scripts and data for analyzing text transformations during the writing process.*

## Overview
This directory contains data and scripts used to analyze the evolution of text through multiple editing stages.  The analysis focuses on word retention, sentence structure, and overall similarity between consecutive versions of a document.  The results are presented in CSV and Markdown files, along with visualizations in a zipped bundle.  This analysis helps to understand the impact of different editing stages on the final product. The provided Python script (though incomplete) was intended to process these data.

## Contents
- `Article_metrics__by_stage_.csv` — Metrics (words, sentences, etc.) for each article stage.
- `ChatGPT-Python analysis results.md` — ChatGPT's analysis of the Python script and its limitations.
- `Consecutive_version_retention___similarity.csv` — Word and sequence similarity between consecutive versions.
- `Pairwise_cosine_similarity__TF-IDF_.csv` — Pairwise cosine similarity scores using TF-IDF.
- `base_agg.csv` — Aggregated metrics across all version comparisons.
- `charts_bundle.zip` — Contains visualization charts (png files).


## Quick Start
The Python script (`0510-generate-data.py`, not included) was designed to process the article files.  Due to incompleteness, execution requires patching and completion of the script. Results were partially generated via ChatGPT.

## Conventions
CSV files use commas as separators.  Chart filenames in `charts_bundle.zip` describe the visualized data.

---
Last updated: 2025-09-13
