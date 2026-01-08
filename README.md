Perfect — below is a **clean, professional, judge-ready README.md** you can **directly paste** into your repository and commit.

This README is written to:

* satisfy **Track A requirements**
* look strong to **hackathon evaluators**
* be understandable even if the reader never saw the problem statement

---

# 📘 Narrative Consistency Reasoning Engine

**Kharagpur Data Science Hackathon 2026 – Track A Submission**

---

## 🧠 Overview

Large Language Models often fail at **global consistency reasoning** over long narratives.
They generate locally plausible explanations that break **causal constraints**, **timelines**, or **character evolution** established earlier in the text.

This project implements a **Narrative Consistency Reasoning Engine** that explicitly addresses this limitation.

### 🎯 Objective

Given:

* a **full long-form narrative** (100k+ words, unabridged)
* a **hypothetical character backstory** (not part of the novel)

The system determines whether the backstory is:

* **Consistent (1)** or
* **Inconsistent (0)**
  with the narrative as a whole.

This is treated as a **decision and reasoning problem**, not text generation.

---

## 🏁 Hackathon Track

* **Event:** Kharagpur Data Science Hackathon 2026
* **Track:** **Track A – Systems Reasoning with NLP & Generative AI**
* **Focus Areas:**

  * Long-context handling
  * Evidence aggregation
  * Causal and temporal reasoning
  * Robust, reproducible system design

---

## 🧩 System Architecture

```
Narrative Text (Novel)
        ↓
Backstory Decomposition
        ↓
Claim-wise Evidence Retrieval
        ↓
Temporal & Causal Constraint Analysis
        ↓
Global Consistency Aggregation
        ↓
Binary Decision (0 / 1)
```

The system avoids surface-level plausibility and instead reasons over **constraints accumulated across the narrative**.

---

## 🔬 Reasoning Pipeline

### 1️⃣ Backstory Decomposition

The backstory is decomposed into **atomic, falsifiable claims**, such as:

* early-life events
* beliefs and fears
* motivations and commitments

Each claim is independently verifiable.

---

### 2️⃣ Long-Context Evidence Retrieval

For every claim, the system retrieves **multiple relevant passages** from different parts of the narrative that may:

* support the claim
* contradict it
* impose constraints on it

This prevents cherry-picking and encourages global reasoning.

---

### 3️⃣ Constraint & Causal Analysis

Each claim is evaluated across four dimensions:

* timeline alignment
* causal feasibility
* character evolution consistency
* world-rule and setting constraints

Claims are classified as:

* **SUPPORTED**
* **CONTRADICTED**
* **WEAKLY_CONSTRAINED**
* **NOT_CONSTRAINED**

---

### 4️⃣ Global Aggregation Logic

Decision rule:

* **If any claim is CONTRADICTED → Backstory is Inconsistent (0)**
* Otherwise → **Consistent (1)**

This mirrors the official evaluation definition.

---

## 📁 Project Structure

```
Narrative-Consistency-Reasoning-Engine/
│
├── src/
│   ├── main.py              # CLI entry point
│   ├── pipeline.py          # Orchestrates the full reasoning process
│   ├── models.py            # Data models
│   ├── interfaces.py        # LLM abstraction (real + mock)
│   ├── gemini_llm.py        # Gemini LLM integration
│   └── stages/
│       ├── decomposition.py # Backstory → claims
│       ├── retrieval.py     # Evidence retrieval
│       ├── analysis.py      # Constraint analysis
│       └── aggregation.py   # Final decision logic
│
├── tests/                   # Unit tests for each stage
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Run the Engine

Prepare two files:

* `narrative.txt` → full novel text
* `backstory.txt` → hypothetical backstory

Run:

```bash
python -m src.main --n narrative.txt --b backstory.txt
```

**Output:**

```
Consistency Judgment: 1  (or 0)
```

---

## 🧪 Testing

Unit tests are provided to validate each reasoning stage.

Run:

```bash
pytest
```

All stages (decomposition, retrieval, analysis, aggregation) are independently tested for correctness.

---

## 🤖 LLM Usage

* The system supports **real LLMs** (e.g., Gemini)
* A **MockLLM** is included for:

  * offline testing
  * reproducibility
  * debugging without API keys

This design ensures the pipeline logic is evaluated independently of model fluency.

---

## 📊 Output Format

The system produces:

* a **binary prediction** (0 / 1)
* optionally, a **concise evidence-based rationale**

This aligns with the official `results.csv` submission format.

---

## ⚠️ Known Limitations

* Very subtle implicit constraints may be missed
* Performance depends on evidence retrieval quality
* Extremely ambiguous narratives may lead to weakly constrained outcomes

These limitations are documented transparently, as encouraged by the evaluation guidelines.

---

## ✅ Alignment with Evaluation Criteria

✔ Explicit reasoning over long contexts
✔ Evidence-grounded decisions
✔ Robust aggregation logic
✔ Reproducible and modular system
✔ Focus on reasoning quality over generation fluency

---

## 📌 License

MIT LICENSE

---

