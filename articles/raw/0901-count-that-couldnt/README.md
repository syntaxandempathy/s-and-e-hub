# The Count That Couldn't: Tracking AI and Human Contributions in Writing

*A chronicle of building (and breaking) a tool to measure human contributions in AI-assisted writing.*

## Overview
This directory contains the documentation and materials from a series of experiments aimed at building a tool to quantify the balance between human and AI contributions during the writing process.  The project involved several iterations, using various approaches including JSON/XML, and ultimately Python scripting.  The documentation includes articles detailing the successes and failures encountered, along with the scripts and data generated during the testing phase.  This repository serves as a record of the journey and its lessons.

## Contents
* `01-the-count-that-coudnt.md` — First article in a series documenting the challenges of building the tool.
* `02-the-count-that-coudnt.md` — Second article detailing the shift to Python.
* `03-the-count-that-coudnt.md` — Third article reflecting on the collapse of the first attempt.
* `04-the-count-that-coudnt.md` — Fourth article highlighting the costs of inadequate planning.
* `materials/0510-ai_script_reflection_full_with_appendix.md` — Reflection on using AI to generate Python code.
* `materials/0510-chatgpt-ai-script-debugging-analysis.md` — Analysis of AI-generated Python debugging process.
* `materials/0510-generate-data.py` — Python script for analyzing text data.
* `materials/0513-chatgpt-human-contribution-metrics-charts.md` — ChatGPT conversation on visualizing metrics.
* `materials/0513-compare-data.py` — Python script for data comparison and visualization.
* `materials/ChatGPT-Python File Analysis.md` — ChatGPT conversation analyzing Python file for file path issues.
* `materials/script-test-2/*` — Data and results from the second script test run.
* `materials/script-test-3/*` — Data and results from the third script test run.


## Quick Start
The Python scripts (`materials/0510-generate-data.py`, `materials/0513-compare-data.py`) require Python and several libraries (including `pandas`, `sklearn`, `matplotlib`).  Adapt file paths within the scripts to match your data.  The scripts process markdown files to generate various metrics and visualizations.  Consult the accompanying documentation for detailed explanations.


## Conventions
The `materials` directory is organized by date and contains subdirectories for each script test iteration.  CSV files store the generated data, while markdown files document the processes and analyses.


---
Last updated: 2025-09-13
