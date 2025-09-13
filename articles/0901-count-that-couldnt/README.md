# The Count That Couldn't: Measuring Human Contributions in AI-Assisted Writing

*A chronicle of attempts to build a tool for tracking human edits in AI-generated text.*

## Overview
This directory contains the documentation and materials from a series of experiments aimed at creating a tool to measure the extent of human contributions when using AI for writing.  The project involved several iterations, using different approaches and tools, ultimately culminating in a functional Python script and accompanying data analysis. The markdown files detail the process, challenges, and lessons learned throughout the development. This repository serves as a detailed record of this iterative process, including code, data, and analysis.

## Contents
* `01-the-count-that-coudnt.md` — The first article in a series documenting the project's journey.
* `02-the-count-that-coudnt.md` — Further details on early challenges and the shift to Python.
* `03-the-count-that-coudnt.md` — A comprehensive overview of the project's first failed attempt.
* `04-the-count-that-coudnt.md` — Additional reflections on the project's initial challenges and lessons learned.
* `materials/0510-ai_script_reflection_full_with_appendix.md` — Reflections on using AI to generate the Python scripts.
* `materials/0510-chatgpt-ai-script-debugging-analysis.md` — Detailed analysis of AI-generated code debugging sessions.
* `materials/0510-generate-data.py` — The core Python script used to generate metrics from text files.
* `materials/0513-chatgpt-human-contribution-metrics-charts.md` —  ChatGPT prompts and responses for generating charts.
* `materials/0513-compare-data.py` — Python script for generating visualizations.
* `materials/ChatGPT-Python File Analysis.md` — Analysis of a ChatGPT session regarding the Python script.
* `materials/script-test-2/*` — Data and results from the second script testing phase.
* `materials/script-test-3/*` — Data and results from the third script testing phase.


## Quick Start
To reproduce the analysis, you will need to install the required Python libraries (pandas, scikit-learn, matplotlib).  Then, modify file paths within `materials/0510-generate-data.py` to point to your markdown files and execute the script.  The generated data will then be used in `materials/0513-compare-data.py` to produce charts.

## Conventions
The `materials` directory is structured by date and contains various iterations of scripts, data files (CSV), and ChatGPT conversation logs (Markdown).  Each script test subdirectory contains the generated CSV data and visualization outputs (ZIP).

---
Last updated: 2025-09-13
