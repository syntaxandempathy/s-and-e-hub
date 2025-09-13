# Materials: AI-Assisted Document Version Comparison Analysis

*This directory contains data and scripts used to analyze the evolution of documents across multiple versions using AI-generated Python code.*

## Overview
This directory holds materials from an experiment in using AI to generate Python code for analyzing document versions.  The experiment involved generating Python scripts to compare different versions of a document, measure changes, and visualize the results.  Multiple iterations of the scripts and their outputs are included, along with supporting documentation detailing the process and insights gained.  The data can be used to understand the effectiveness of AI in automating such analyses and highlight challenges encountered.

## Contents
- `0510-ai_script_reflection_full_with_appendix.md` — Reflection on the AI script development process.
- `0510-chatgpt-ai-script-debugging-analysis.md` — Detailed analysis of debugging challenges with AI-generated code.
- `0510-generate-data.py` — Initial Python script for generating comparison data.
- `0513-chatgpt-human-contribution-metrics-charts.md` — Specifications and discussion of human contribution metrics charts.
- `0513-compare-data.py` — Python script for analyzing and visualizing comparison data.
- `ChatGPT-Python File Analysis.md` — ChatGPT analysis of a Python file used in the project.
- `script-test-1/`, `script-test-2/`, `script-test-3/` — Subdirectories containing data and results from different test runs.


## Usage
The Python scripts (`0510-generate-data.py`, `0513-compare-data.py`) require Python 3 and several libraries (pandas, scikit-learn, matplotlib).  Adapt file paths within the scripts to point to your data files.  Run the scripts to generate and analyze document comparison data.  The results will be saved in CSV files and optionally visualized as charts (within the `script-test-*` directories).

## Conventions
Each subdirectory (`script-test-1`, `script-test-2`, `script-test-3`) represents a separate experiment run, containing data files, analysis results, and generated charts.  Data files are primarily CSV formatted for easy analysis with spreadsheets and other tools.

---
Last updated: 2025-09-13
