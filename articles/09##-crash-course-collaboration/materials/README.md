# Materials for AI Writing Analysis

*Supporting files and scripts for an AI writing analyzer.*

## Overview
This directory contains input data, Python scripts, and output reports related to an analysis of AI-generated text across different revision stages.  The analysis focuses on metrics such as word count, sentence length, vocabulary changes, and semantic similarity between stages. The Python script `0610-ai-writing-analyzer-enhanced.py` performs the core analysis, producing CSV and markdown reports.  Input data includes several CSV files detailing the characteristics of different stages of text.

## Contents
* `code/0610-ai-writing-analyzer-enhanced.py` — Python script to analyze text across revision stages.
* `code/output/ChatGPT-Article version analysis.md` — ChatGPT-generated analysis report.
* `code/output/markup-languages-analysis-report.md` — Markdown report summarizing the analysis of a "Markup Languages" article.
* `code/output/markup-languages-stage-metrics.csv` — CSV of stage-wise metrics for the "Markup Languages" article.
* `code/output/markup-languages-transition-analysis.csv` — CSV detailing transitions between stages for the "Markup Languages" article.
* `input/0610-chatgpt-ai-writing-analyzer-help.md` — ChatGPT help file for using the analyzer.
* `input/0610-semantic_similarity_between_stages.csv` — CSV of semantic similarity scores between stages.
* `input/0610-stage_metrics.csv` — CSV of stage-wise metrics.
* `input/0610-topic_distributions_by_stage.csv` — CSV of topic distributions by stage.
* `input/0610-transition_analysis.csv` — CSV of transition analysis.


## Quick Start
To run the analysis, ensure you have the necessary Python libraries installed (`pandas`, `scikit-learn`).  Then, execute the script `code/0610-ai-writing-analyzer-enhanced.py`, providing paths to your input files as needed. Output files will be generated in the `code/output` directory.  Refer to `input/0610-chatgpt-ai-writing-analyzer-help.md` for detailed instructions.


## Conventions
Input data is organized in CSV files, with each file representing a specific aspect of the analysis (e.g., stage metrics, transition analysis). Output is generated as both CSV and Markdown files for easy consumption and further analysis.


---
Last updated: 2025-09-05
