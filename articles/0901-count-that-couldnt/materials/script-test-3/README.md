# script-test-3

*A collection of scripts and data for analyzing text transformations during article editing.*

## Overview
This directory contains Python scripts and CSV data files used to analyze the textual evolution of an article across multiple editing stages (draft, refined, edited, final).  The analysis includes metrics such as word count, sentence count, unique word counts, and pairwise similarity scores calculated using TF-IDF cosine similarity and difflib ratio.  The results are presented in CSV format and visualized in a bundled chart archive.  This repository facilitates the quantitative assessment of editorial changes and the impact of AI-assisted writing.

## Contents
* `Article_file_basic_counts.csv` — Basic metrics (characters, words, sentences) for each article version.
* `ChatGPT-Run python on articles.md` — ChatGPT conversation detailing the execution of the Python analysis script.
* `Pairwise_TF-IDF_cosine_similarity.csv` — Pairwise cosine similarity scores between article versions using TF-IDF.
* `Pairwise_difflib_ratio.csv` — Pairwise similarity ratios between article versions using difflib.
* `Per-stage_metrics.csv` — Per-stage metrics (characters, words, sentences, unique words, average sentence length).
* `Token_retention_transitions.csv` — Token retention percentages across editing stages.
* `Uploaded_files__quick_preview.csv` — Metadata and preview of uploaded files used in the analysis.
* `base_agg.csv` — Aggregate metrics summarizing changes across versions.
* `charts_bundle.zip` —  Zipped archive containing visualizations of the analysis results (images).
* `0510-generate-data.py` — Python script for performing the analysis.


## Quick Start
To reproduce the analysis, ensure you have the necessary Python libraries installed (pandas, scikit-learn, difflib). Then, run the `0510-generate-data.py` script.  The script processes the article files and generates the CSV output files.  Visualization requires separate software; image files are located in charts_bundle.zip.


## Conventions
CSV files use the first row as a header.  The Python script is designed to be modular and easily adaptable to different input files by adjusting file paths within the script.


---
Last updated: 2025-09-13
