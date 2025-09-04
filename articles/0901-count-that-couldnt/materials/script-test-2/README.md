# Quantitative Analysis of Article Revisions
*A Python script analyzes four article versions (draft to final) and generates charts illustrating the impact of each editing stage.*

**Overview**

This repository contains the data and analysis of an article's evolution through four revision stages: draft, refined, edited, and final.  A Python script (0510-generate-data.py) calculates metrics such as word retention, sequence similarity, and cosine similarity.  The results are presented in CSV files and visualized in interactive charts (charts_bundle.zip). This README provides an overview of the project and its findings.  The analysis helps quantify the effects of each editing phase.


**Contents**

* `0510-generate-data.py`: Python script for article analysis.
* `Article_metrics__by_stage_.csv`: Article metrics for each revision stage.
* `Consecutive_version_retention___similarity.csv`: Word and sequence similarity between consecutive versions.
* `Pairwise_cosine_similarity__TF-IDF_.csv`: Pairwise cosine similarity using TF-IDF.
* `base_agg.csv`: Aggregated metrics across all versions.
* `charts_bundle.zip`:  Archive containing interactive charts visualizing the analysis results.
* `meta.yml`: Project metadata and description.


**Usage**

To reproduce the analysis, ensure you have Python 3 installed along with the necessary libraries (as specified in `0510-generate-data.py`).  Place the four article files (draft-article.md, refined-article.md, edited-article.md, final-article.md - not included here) in the same directory as the script.  Run the script using: `python 0510-generate-data.py`.  The results will be saved as CSV files in the current directory.  The charts can then be viewed by unzipping the `charts_bundle.zip` file.


**Structure**

The repository is organized into data files (CSV), a Python analysis script,  a bundle of charts, and metadata files.  CSV files are named to clearly indicate the type of analysis performed.


**Changelog**

Last updated: 2025-09-04
