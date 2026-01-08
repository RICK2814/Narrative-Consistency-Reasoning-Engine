# Narrative Consistency Reasoning Engine

A decision-making engine that validates character backstories against complete long-form narratives.

## Mission
Determine whether a hypothetical character backstory is causally and logically compatible with a complete long-form narrative.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.pipeline import ConsistencyEngine
from src.interfaces import MockLLM

engine = ConsistencyEngine(llm=MockLLM())
result = engine.run(narrative_text="...", backstory="...")
print(result.consistency_judgment)  # 1 or 0
```

## Pipeline Stages
1. **Backstory Decomposition** - Transform backstory into atomic, falsifiable claims
2. **Long-Context Evidence Retrieval** - Locate relevant narrative passages
3. **Temporal and Causal Constraint Analysis** - Evaluate claim compatibility
4. **Global Consistency Aggregation** - Final consistency judgment
Summary
Built a complete Python implementation of the Narrative Consistency Reasoning Engine — a decision-making system that validates character backstories against long-form narratives.

GitHub Repository

src/
├── models.py            # data models for narrative/backstory/results
├── interfaces.py        # LLM adapter abstraction (including a mock LLM)
├── gemini_llm.py        # real LLM integration (Google Gemini)
├── pipeline.py          # main reasoning engine core
├── main.py              # CLI to run the tool
└── stages/
    ├── decomposition.py # stage 1
    ├── retrieval.py     # stage 2
    ├── analysis.py      # stage 3
    └── aggregation.py   # stage 4
tests/
├── test_pipeline.py
└── test_stages.py
README.md
requirements.txt

Pipeline Stages
Stage	Module	Purpose
1	
decomposition.py
Transform backstory → atomic claims
2	
retrieval.py
Find evidence from narrative
3	
analysis.py
Classify each claim
4	
aggregation.py
Apply hard/soft rules for verdict
LLM Providers
MockLLM: For testing, returns pre-canned responses
GeminiLLM: Real reasoning using Google Gemini API
Usage
# Set API key
set GEMINI_API_KEY=your_key_here
# Run with Gemini
python -m src.main -n narrative.txt -b backstory.txt
# Run with Mock (for testing)
python -m src.main -n narrative.txt -b backstory.txt --mock
Test Results
All 13 unit tests pass ✓
