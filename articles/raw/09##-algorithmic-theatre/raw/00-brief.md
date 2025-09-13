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
   - **The Pragmatic Bridge-Builder** — needs realistic tool comparisons, lightweight standards, and small-team playbooks.
**Article Template**
   - **lighter-experiment.md** - For single demonstrations of a method or workflow. (1,200–1,600 words)
**Key Sources:**
   - briefing.md
   - article-series.md - Article 2
   - timeline.md
   - tech.md
   - faq.md
   - 00-rough.md (details)
   - **0606-ai-writing-analyzer.py** – Early Python analyzer: computes per-stage metrics (char/word counts, diffs, simple theme shifts) and overall similarity; serves as a compact rebuild of the missing “compare” step.
   - **0606-ai-writing-tracker.html** – Browser-based manual tracker: log prompts, time, word counts, and notes across five stages; generates a plain-text transparency report (localStorage, no backend).
   - **0606-markup\_analysis\_results.json** – JSON dump from a run of the analyzer (Draft → Refined → Edited → Final) with counts, insert/delete/replace tallies, vocab shifts, simple theme deltas, and structure metrics.
   - **0604-transcript-1.md** – Exploration/working transcript describing the shift in approach, UI quirks while testing a web analyzer, and the need for clearer definitions/metrics for semantic change. Useful as context for why the 0606 tools exist.
   - **0606-chatgpt-clarification-of-request.md** – Short ChatGPT session notes around “turn this / run it,” showing the analyzer’s interactive prompts and the need to pass stage files; helps explain execution friction and subsequent tweaks.
   - **0606-claude-authenticity-.md** – Claude session that produced the self-serve **HTML tracker** concept and markup (the manual disclosure tool that complements the Python analyzer).
   - **app.py** – Flask backend: exposes an /authenticity API endpoint that compares four document stages (AI Draft → AI Refined → Human Edited → Final). Uses NLTK for sentence parsing and a SentenceTransformer model for semantic change. Returns JSON with metrics (word/sentence/paragraph deltas, retention, semantic change).
   - **index.html** – Frontend client: polished web UI for the “Document Delta Analyzer.” Lets you paste/upload four versions of a text, sends them to the backend, and displays checkpoint-by-checkpoint metrics plus workflow summaries.
**Objective:**
Author an unbiased article based on the this brief and the activities or information specified within it. The addition of content based on assumption, extrapolation, or similar forms of fabrication are STRICTLY FORBIDDEN.