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
