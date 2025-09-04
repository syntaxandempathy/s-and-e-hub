# Article Revision Metrics & Analysis
*This repository contains data and analysis of an article's evolution through multiple revision stages.*

**Overview**

This directory houses the data and analysis results for a single article undergoing four revision stages: Draft, Refined, Edited, and Final.  The analysis quantifies changes in word count, sentence structure, vocabulary, and overall similarity between revisions.  Cosine similarity scores and word retention rates are calculated.  Visualizations (in `charts_export.zip`) complement the data tables.  This analysis helps understand the impact of each editing stage.

**Contents**

* `Article_Stage_Metrics.csv`: Summary statistics for each article stage (characters, words, sentences, etc.).
* `ChatGPT-Python script execution results.md`:  Detailed report of the Python script execution and analysis results.
* `Pairwise_Similarity__Cosine__bag-of-words_.csv`: Pairwise cosine similarity between all article stages.
* `Successive_Stage_Word_Retention____.csv`: Word retention percentage between successive article stages.
* `base_agg.csv`: Aggregated metrics showing word, sentence, and paragraph retention across revisions.
* `charts_export.zip`:  Archived folder containing visualizations of the analysis results.
* `meta.yml`: Metadata describing the project, including its purpose and contents.


**Conventions**

Data files use CSV format.  Analysis results are presented in both tabular and visual formats.


Last updated: 2025-09-04
