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

Project Structure
rapid-corona/
├── README.md
├── requirements.txt
├── src/
│   ├── models.py       # Pydantic data models
│   ├── interfaces.py   # LLM abstraction + MockLLM
│   ├── gemini_llm.py   # Google Gemini integration
│   ├── pipeline.py     # Main orchestration
│   ├── main.py         # CLI entry point
│   └── stages/
│       ├── decomposition.py  # Stage 1
│       ├── retrieval.py      # Stage 2
│       ├── analysis.py       # Stage 3
│       └── aggregation.py    # Stage 4
└── tests/
    ├── test_pipeline.py
    └── test_stages.py
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
