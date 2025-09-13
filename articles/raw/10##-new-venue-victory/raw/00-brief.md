# Article Creation Guide

## Objective
Author an unbiased article based on the this brief and the activities or information specified within it. The addition of content based on assumption, extrapolation, or similar forms of fabrication are STRICTLY FORBIDDEN.

## Process
You are expected to adhere to a 6 step process without exception unless explicitly stated by me. The steps within the approaved process are:
1. Review all of the materials specified within this brief.
   - Based on the review, you will generate clarifying questions for the author to resolve ambiguities in the provided materials. You may ask up to 5 questions.
   - The author will provide direct, concise answers to these questions.
   - The author's answers are considered part of the official source material for the article, providing the necessary "narrative glue."
2. Ask clarifying questions to determine narrative structure before writing.
3. Write the initial draft article based request feedback.
4. Update the article, one section at a time, based on:
   - Feedback from step 3 on the initial draft.
   - Feedback provided after the updated sections are provided.
5. After the udpates to the last section have been approved:
   - Provide the fully assembled article within the canvas.
   - Provide recommendations on how the article might be improved.
6. Upon completion of the article provide a downloadable markdown file.

---

## Strategic Direction & Scope
This section provides the mission, audience, and goals of the article.
**Key Constraints & Guardrails**
   - **Source Grounding:** The information used to inform the article MUST be based on the information in this brief or the specified interview and source materials.
   - **Editorial Integrity:** Focus on evidence over hype and honestly include challenges and pitfalls that occured.
   - **Style & Tone:** Your objective is to provide an article with journalistic integrity using the unbiased tone of a documentary. The use of a personal voice, opinions, or unspecified predictions is forbidden.
   - **Article Format:** The final deliverable is a fully written article based on the specified template suitable for publication.
   - **Do Right, Not Easy:** Make ethical choices even when pressured to compromise.
   - **Actively Counter Bias:** Review AI outputs for demographic, cultural, and contextual biases. Document and share mitigation strategies.
   - **Design for the Excluded:** Treat AI failures for specific user groups as a critical bug.
   - **Mentor Through Documentation:** Share knowledge openly to lift up the entire field.
**Content Boundaries**
   - **What You Can Write:** Structure and transitions using provided research, technical explanations from documented sources, process descriptions, research synthesis, and framework development.
   - **What You Cannot Write:** First-person statements, personal anecdotes or stories, industry predictions, or opinions without a documented source.

---

### Why we’re doing this (Strategic intent)
   - **Our mission in action:** Assist creative professionals in the integration of LLMs into their professional processes and workflows through practical guidance, transparent knowledge-sharing, and ethical frameworks.
   - **Vision we’re working toward:** A design landscape where AI augments human capability, and designers navigate emerging tech with confidence, craft, and care.
   - **Positioning we hold:** A design-technology veteran translating complex AI into usable frameworks for UX teams operating in real constraints.

### For whom (Audience archetypes)
   - **The Strategic Orchestrator** — needs governance models, proof of efficiency/ROI, and risk-aware adoption strategies.
   - **The Emerging Practitioner** — needs tutorials, templates, and portfolio-safe case studies to build skills.
   - **The Holistic Thinker** — needs tools for systemic risk mapping, bias mitigation, and establishing ethical benchmarks.
   - **The Agency Systematizer** — needs repeatable workflows, automation playbooks, and QA/governance processes.
   - **The Pragmatic Bridge-Builder** — needs realistic tool comparisons, lightweight standards, and small-team playbooks.

### Problems we exist to solve (Reader pain points)
   - **Instruction & Intentionality Gap:** Bridging the gap between nuanced design intent and the **unambiguous instructions** necessary for clear communication with AI models, especially across multi-turn interactions.
   - **“AI Tax” & Quality Deficit:** Overcoming the **"AI Tax"**—the high cost of rework and refinement needed to elevate generic AI outputs to a professional standard of quality and nuance.
   - **Workflow Fragmentation:** **Architecting coherent workflows** that integrate disparate AI tools into a seamless and efficient design process.
   - **Ethical & Reliability Risk:** **Managing the inherent risks** of AI, including algorithmic bias, factual hallucinations, and opacity, to ensure responsible and reliable outcomes.
   - **Skill & Role Evolution:** Navigating the **professional evolution** from tactical execution to strategic oversight, including the curation of AI outputs and the stewardship of human-centered design principles.

### What “good” looks like (Acceptance Criteria & Quality Gate)
   - Educational value for professionals
   - Provides actionable artifacts
   - Addresses ethics and risk
   - Specifies evaluation and limits

---

## Article & Sources
**Topic:**
A Comparative Analysis of AI-Powered Usability Testing Tools.
**Target Archetypes:**
   - **The Emerging Practitioner** — needs tutorials, templates, and portfolio-safe case studies to build skills.
   - **The Holistic Thinker** — needs tools for systemic risk mapping, bias mitigation, and establishing ethical benchmarks.
   - **The Agency Systematizer** — needs repeatable workflows, automation playbooks, and QA/governance processes.
   - **The Pragmatic Bridge-Builder** — needs realistic tool comparisons, lightweight standards, and small-team playbooks.
**Article Template**
   - **detailed-experiment.md** - For full documentation of structured experiments. (1,800–2,500 words)
**Key Sources:**
   - briefing.md
   - article-series.md - Article 4
   - timeline.md
   - tech.md
   - faq.md
   - 00-rough.md (details)
   - 0614-transcript-2.md: your running commentary while shifting the pipeline into Colab, describing multi-step processing, saved artifacts, and the move toward semantics (not just counts).
   - Claude-Python NLP Research in Colab.md: the back-and-forth planning/spec for a Colab-orchestrated, stepwise pipeline (free tooling, Drive I/O, checkpoints).
   - Artifacts produced by that Colab run (same article: “markup-languages”)
       - markup-languages_checkpoint_steps_1_2.json: the Step 1–2 checkpoint showing versions found (draft/refined/edited/final), counts, and validation. 
       - markup-languages_complete_analysis.json: the full output with lexical+semantic similarity (incl. sentence-level matches) across version pairs. 
       - markup-languages_footer_metrics.json: the lightweight, publishable metrics (e.g., overall similarity 43.1%, origins like Edited 85.7%, Draft 2.4%) intended for article footers.

**Colab Notebooks (ai-vs-human series)**
   - **`ai-vs-human-v0.1.ipynb`**
        * **Purpose:** Very first exploratory notebook.
        * **Likely contents:**
          * Loads draft/refined/edited/final markdowns.
          * Basic word/character counts, maybe a difflib similarity check.
          * Early proof-of-concept for comparing human vs. AI contribution.
        * **Limitations:** Rudimentary metrics, little structure. Output probably inline printouts, not saved files.
   - **`ai-vs-human-v0.2.ipynb`**
        * **Purpose:** First structured attempt at a **pipeline**.
        * **Changes from v0.1:**
          * Added *stage-by-stage analysis* with proper dataframes.
          * Introduced similarity measures beyond raw counts (cosine/Tf-idf).
          * Started exporting partial results, which evolve into the JSON checkpoint files.
        * **Significance:** This is where the idea of **checkpoints** likely emerged, but not yet consistently saved.
   - **`ai-vs-human-v0.3.ipynb`**
        * **Purpose:** Refinement into a **multi-step pipeline** with modular steps.
        * **Changes from v0.2:**
          * Split into distinct stages (Step 1: load + clean, Step 2: metrics, Step 3: transitions, Step 4: semantics).
          * Introduced per-transition metrics and retention.
          * Experimented with sentence-level semantic similarity and possibly topic modeling.
        * **Significance:** Precursor to the 0614 JSONs — “checkpoint steps” and “complete analysis” emerge here.
   - **`ai-vs-human.ipynb` (almost final)**
        * **Purpose:** Polished notebook used to generate the stable JSON outputs.
        * **Changes from v0.3:**
          * Standardized outputs:
            * **Checkpoint JSON** → basic metrics & validation of stages.
            * **Complete analysis JSON** → full lexical + semantic comparisons, including sentence matches.
            * **Footer metrics JSON** → compressed, reader-facing disclosure values.
          * Cleaner data structures, suitable for saving and re-using.
        * **Significance:** This is the notebook that directly produced the **0614 artifacts** (`markup-languages_checkpoint_steps_1_2.json`, `markup-languages_complete_analysis.json`, `markup-languages_footer_metrics.json`).

**Objective:**
Author an unbiased article based on the this brief and the activities or information specified within it. The addition of content based on assumption, extrapolation, or similar forms of fabrication are STRICTLY FORBIDDEN.