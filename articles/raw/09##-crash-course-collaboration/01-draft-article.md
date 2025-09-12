# Article 3 — Enhanced Analyzer + Outputs (0610)

---

### Intro / Hook

By mid-June 2025, the experiment to measure human and AI contribution in writing had reached a turning point. Earlier attempts using sprawling JSON and XML structures collapsed under their own weight: inconsistent formats, broken visualizations, and divergent outputs that grew useless the moment real data was applied.

This new phase, centered on the file `0610-ai-writing-analyzer-enhanced.py`, marked the first time the analyzer matured into something structured and reproducible. It produced clean metrics, exported data as CSV and JSON, and incorporated the first semantic similarity comparisons that truly clarified how a draft evolved into a final piece.

The journey was far from smooth. LDA topic modeling confused more than it illuminated, AI assistance remained unreliable, and the human guiding the project still had no grounding in Python. As the User reflected:

> *“I had, up to the point I started asking questions, my own worst enemy.”*

Yet persistence transformed failure into function. This stage laid the groundwork for the reproducible Colab pipeline that followed, proving that even inexpert humans could push AI into producing useful, ethical analysis tools.

---

### Setup

The immediate backdrop was failure.

* The **JSON framework** ballooned past 11,000 characters, stripped too much context, and collapsed as soon as real article data was tested.
* The **XML alternative** hit context limits.
* Attempts at **multi-AI peer review** (Claude and GPT critiquing each other) devolved into loops of contradictory rationales.

At \~2:30 a.m., a realization set in: the frameworks weren’t failing at design, they were failing under *real inputs*. The solution was a **pivot to Python**, suggested by Claude but executed entirely through AI-generated code, since the User could not program themselves.

This created an unusual dynamic:

* The **AI wrote the code**, often confidently but incorrectly.
* The **User provided oversight**, asking increasingly explicit questions to catch errors.
* At this moment in time, AI-written code was only just beginning to emerge as a widespread practice.

Two scripts were envisioned: one to **generate metrics** from multiple versions of a document, and another to **compare stages**. The generator stabilized quickly. The comparator proved fragile, with functions disappearing, phantom imports, and persistent misdirection from AI.

By early June, after weeks of debugging, the **enhanced analyzer** emerged. It was the first tool in this series to combine stability, structure, and semantic awareness.

---

### Execution

#### The Enhanced Analyzer Script

The file `0610-ai-writing-analyzer-enhanced.py` consolidated weeks of iteration. Its core functions included:

* **Stage Metrics:** Calculated character count, word count, and average sentence length across Draft, Refined, Edited, and Final versions.
* **Transition Analysis:** Measured sequence similarity (via `difflib`), percentage change in word count, and vocabulary churn (new terms introduced at each stage).
* **Draft→Final Semantic Similarity:** Introduced for the first time. Using TF-IDF and cosine similarity, the analyzer quantified how much meaning carried across the entire journey.

Structured outputs were now possible: CSVs and JSONs that archived results in AI-readable form for reproducibility.

Insert code snippet from analyzer here

#### Outputs in Practice

Running the analyzer on four article stages produced tables that revealed the editorial rhythm:

**Stage Metrics**
Insert `stage_metrics.csv` table here

**Transition Analysis**
Insert `transition_analysis.csv` table here

**Semantic Similarity**

* Draft → Refined: \~81%
* Refined → Edited: \~68%
* Edited → Final: \~89%
* Draft → Final: \~61%

This was the first time the process yielded both interpretable numbers and reusable data.

#### The Dialogue of Refinement

The path to these results required negotiating with AI systems that were themselves inconsistent.

* **Topic Modeling (LDA):** Initially attempted to detect thematic drift. Instead, every document collapsed into near-singular topics. The User noted it was “essentially a keyword search” and abandoned it as unhelpful.
* **TF-IDF + Cosine Similarity:** A breakthrough. Unlike LDA, it offered clear percentages that directly answered whether a revision changed meaning or simply cleaned up language.
* **Sentence-BERT (SBERT):** Identified as superior, but unavailable in the sandbox. Workarounds were drafted for running SBERT in Google Colab or GitHub Codespaces, though dependency errors (“GenerationMixin,” “cached\_download”) required pinning versions of `transformers` and `huggingface_hub`.

The analyzer became not just a script, but a **conversation with AI** about what constituted meaningful change, and which methods were transparent enough to trust.

---

### Findings

#### A Rhythm of Expansion, Pruning, and Polish

The enhanced analyzer quantified editorial dynamics that had previously been anecdotal:

* **Draft → Refined:** Expansion. Word count jumped \~69%, introducing nearly 300 new terms. Semantic similarity (\~81%) showed the base ideas carried through, but the scope expanded dramatically.
* **Refined → Edited:** Pruning. Word count dropped \~34%. Similarity fell to \~68%, reflecting heavy restructuring and removal of tangents. \~126 new terms entered, but the document’s architecture shifted most.
* **Edited → Final:** Polish. Similarity rose to \~89% with only a 5% word count trim. This was cleanup, smoothing, and phrasing adjustments.
* **Draft → Final:** Just \~61% semantic overlap remained — proof of how far the final text had moved from its origin.

#### Conceptual Comparisons

* **LDA vs TF-IDF:** LDA highlighted the limits of opaque algorithms. TF-IDF provided clarity and interpretability.
* **TF-IDF vs SBERT:** TF-IDF worked and was reproducible. SBERT promised more nuanced semantic fidelity once technical barriers were overcome.
* **Structured Exports vs Ad-hoc Results:** For the first time, results were reproducible. CSVs and JSONs meant the analyzer could be rerun, compared over time, and shared with others.

#### Emotional & Methodological Insights

The technical gains sat alongside human lessons:

* AI often delivered code that looked correct but wasn’t.
* The User, lacking Python experience, had to become a detective, spotting silent failures and regressions.
* Persistence mattered more than expertise. Asking sharper questions forced the AI into producing functional solutions.

The analyzer was no longer just an experiment in metrics; it was proof of how non-technical users could negotiate with AI to produce transparent, ethical analysis tools.

---

### Takeaways

* **Structured outputs were transformative.** CSV and JSON exports marked the transition from fragile prototypes to repeatable analysis.
* **AI-generated code was viable but fragile.** At a time when this was just emerging, oversight and constant questioning were essential.
* **Conceptual comparisons mattered.** The journey from LDA → TF-IDF → SBERT clarified both technical trade-offs and the trajectory toward more meaningful metrics.
* **The human role shifted.** From “own worst enemy” to persistent questioner, the User learned that success meant interrogating AI, not trusting it blindly.

---

### Practical Next Steps

For practitioners and teams considering similar work:

* **Baseline:** Use TF-IDF + cosine similarity as a clear, reproducible method for measuring semantic change.
* **Advanced:** Explore SBERT or embedding APIs once infrastructure allows. Pin dependencies to avoid errors.
* **Workflow design:** Always output structured files (CSV/JSON) for reproducibility and long-term comparison.
* **Integration:** Treat this kind of analyzer as a stepping stone toward more polished pipelines, such as those later built in Google Colab.

Insert downloadable links here: enhanced analyzer script, CSVs, high-res charts

---

### Closing Reflection

This stage did not deliver perfection. Topic modeling floundered, SBERT proved elusive, and debugging was constant. But the analyzer crossed a threshold: it produced **structured, interpretable, reproducible outputs**.

From here, the project could evolve into a full pipeline. The analyzer had moved from fragility to function — not flawless, but finally usable.