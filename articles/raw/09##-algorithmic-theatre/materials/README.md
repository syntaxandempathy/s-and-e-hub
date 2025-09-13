# AI Writing Process Materials

*A collection of scripts and documents for analyzing and tracking the AI writing process.*

## Overview
This directory contains materials related to analyzing and tracking the stages of AI-assisted writing.  It includes Python scripts for analyzing text changes between writing stages, HTML and JavaScript for a process tracker, and various supporting documents such as transcripts and analysis results.  These tools help measure the impact of AI assistance and maintain ethical transparency in the writing process. The materials are designed to be easily accessible and used by both developers and non-developers.  The core functionality revolves around comparing different text versions to identify changes and provide metrics on the writing process.

## Contents
* `0604-transcript-1.md` — Transcript of a discussion about the AI writing process and its analysis.
* `0606-ai-writing-analyzer.py` — Python script to analyze text changes across writing stages.
* `0606-ai-writing-tracker.html` — HTML/JS web application for tracking the AI writing process.
* `0606-chatgpt-clarification-of-request.md` — Record of clarifying a request for the `ai-writing-analyzer.py` script.
* `0606-claude-authenticity-.md` — Notes on maintaining authenticity when using AI in writing.
* `0606-markup_analysis_results.json` — JSON file containing results of a markup analysis.
* `app.py` — Flask application for semantic analysis of text.
* `index.html` — Main HTML file for the document delta analyzer.


## Quick Start

To use the `0606-ai-writing-analyzer.py` script:

1.  Ensure you have Python 3 installed along with the required libraries (mentioned in the script).
2.  Prepare your text files for each writing stage.
3.  Run the script, providing the filepaths as command-line arguments.


## Conventions

The naming convention for files generally follows the format `MMDD-description.filetype`.  JSON files store structured data, while `.md` files contain textual information and transcripts.  Python scripts are designed to be modular and reusable.


---
Last updated: 2025-09-05
