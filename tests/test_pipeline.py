"""
Tests for the Narrative Consistency Reasoning Engine pipeline.
"""

import pytest
from src.pipeline import ConsistencyEngine
from src.interfaces import MockLLM
from src.models import ConsistencyLabel


class TestConsistencyEngine:
    """Test suite for the main pipeline."""

    def test_consistent_backstory_returns_1(self):
        """A backstory with no contradictions should return consistency_judgment=1."""
        llm = MockLLM(force_contradiction=False)
        engine = ConsistencyEngine(llm=llm)
        
        narrative = "Alice fell down the rabbit hole. She met the Cheshire Cat."
        backstory = "Alice was curious as a child. She loved exploring gardens."
        
        result = engine.run(narrative_text=narrative, backstory=backstory)
        
        assert result.consistency_judgment == 1
        assert "consistent" in result.rationale.lower()

    def test_contradicted_backstory_returns_0(self):
        """A backstory with contradictions should return consistency_judgment=0."""
        llm = MockLLM(force_contradiction=True)
        engine = ConsistencyEngine(llm=llm)
        
        narrative = "Alice fell down the rabbit hole. She met the Cheshire Cat."
        backstory = "Alice was curious as a child. She loved exploring gardens."
        
        result = engine.run(narrative_text=narrative, backstory=backstory)
        
        assert result.consistency_judgment == 0
        assert "inconsistent" in result.rationale.lower()

    def test_empty_backstory_is_trivially_consistent(self):
        """An empty backstory should be trivially consistent."""
        llm = MockLLM()
        engine = ConsistencyEngine(llm=llm)
        
        narrative = "Alice fell down the rabbit hole."
        backstory = ""
        
        result = engine.run(narrative_text=narrative, backstory=backstory)
        
        assert result.consistency_judgment == 1
        assert "trivial" in result.rationale.lower()

    def test_claim_analyses_included_in_result(self):
        """Result should include individual claim analyses."""
        llm = MockLLM()
        engine = ConsistencyEngine(llm=llm)
        
        narrative = "Alice fell down the rabbit hole."
        backstory = "Alice was curious. She loved gardens."
        
        result = engine.run(narrative_text=narrative, backstory=backstory)
        
        assert len(result.claim_analyses) > 0
        for analysis in result.claim_analyses:
            assert analysis.claim_id is not None
            assert analysis.label in ConsistencyLabel


class TestAggregationLogic:
    """Test the hard/soft rule aggregation logic."""

    def test_single_contradiction_fails_entire_backstory(self):
        """Even one CONTRADICTED claim should fail the whole backstory."""
        llm = MockLLM(force_contradiction=True)
        engine = ConsistencyEngine(llm=llm)
        
        # Multiple sentences to generate multiple claims
        backstory = "Claim one. Claim two. Claim three. Claim four."
        narrative = "Some narrative text."
        
        result = engine.run(narrative_text=narrative, backstory=backstory)
        
        # Should be inconsistent due to the one contradiction
        assert result.consistency_judgment == 0
        
        # Verify we have multiple claims but only one is contradicted
        contradicted = [
            a for a in result.claim_analyses 
            if a.label == ConsistencyLabel.CONTRADICTED
        ]
        assert len(contradicted) == 1  # MockLLM only contradicts first claim
