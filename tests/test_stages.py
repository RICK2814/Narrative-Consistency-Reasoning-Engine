"""
Tests for individual pipeline stages.
"""

import pytest
from src.stages import (
    BackstoryDecomposer,
    EvidenceRetriever,
    ConstraintAnalyzer,
    ConsistencyAggregator,
)
from src.interfaces import MockLLM
from src.models import BackstoryClaim, ClaimEvidence, ClaimAnalysis, ConsistencyLabel


class TestBackstoryDecomposer:
    """Tests for Stage 1: Backstory Decomposition."""

    def test_decompose_generates_claims(self):
        """Decomposer should generate claims from backstory text."""
        llm = MockLLM()
        decomposer = BackstoryDecomposer(llm=llm)
        
        backstory = "Alice was curious. She loved exploring."
        claims = decomposer.decompose(backstory)
        
        assert len(claims) > 0
        assert all(isinstance(c, BackstoryClaim) for c in claims)

    def test_decompose_empty_backstory_returns_empty(self):
        """Empty backstory should return empty list."""
        llm = MockLLM()
        decomposer = BackstoryDecomposer(llm=llm)
        
        claims = decomposer.decompose("")
        
        assert claims == []


class TestEvidenceRetriever:
    """Tests for Stage 2: Evidence Retrieval."""

    def test_retrieve_returns_evidence_for_claims(self):
        """Retriever should return evidence for each claim."""
        llm = MockLLM()
        retriever = EvidenceRetriever(llm=llm)
        
        claims = [
            BackstoryClaim(claim_id="c1", claim_text="Test claim", claim_type="event")
        ]
        narrative = "Some narrative text with details."
        
        evidence = retriever.retrieve(narrative, claims)
        
        assert len(evidence) == 1
        assert evidence[0].claim_id == "c1"

    def test_retrieve_empty_claims_returns_empty(self):
        """No claims means no evidence."""
        llm = MockLLM()
        retriever = EvidenceRetriever(llm=llm)
        
        evidence = retriever.retrieve("Some narrative", [])
        
        assert evidence == []


class TestConstraintAnalyzer:
    """Tests for Stage 3: Constraint Analysis."""

    def test_analyze_produces_classification(self):
        """Analyzer should classify each claim."""
        llm = MockLLM()
        analyzer = ConstraintAnalyzer(llm=llm)
        
        claims = [
            BackstoryClaim(claim_id="c1", claim_text="Test", claim_type="event")
        ]
        evidence = [ClaimEvidence(claim_id="c1", passages=[])]
        
        analyses = analyzer.analyze(claims, evidence)
        
        assert len(analyses) == 1
        assert analyses[0].label in ConsistencyLabel


class TestConsistencyAggregator:
    """Tests for Stage 4: Aggregation."""

    def test_all_supported_returns_consistent(self):
        """All SUPPORTED claims should result in consistency."""
        aggregator = ConsistencyAggregator()
        
        analyses = [
            ClaimAnalysis(
                claim_id="c1",
                label=ConsistencyLabel.SUPPORTED,
                reasoning="Supported by evidence"
            ),
            ClaimAnalysis(
                claim_id="c2",
                label=ConsistencyLabel.SUPPORTED,
                reasoning="Supported by evidence"
            ),
        ]
        
        verdict = aggregator.aggregate(analyses)
        
        assert verdict.consistency_judgment == 1

    def test_any_contradicted_returns_inconsistent(self):
        """Any CONTRADICTED claim should fail the entire check."""
        aggregator = ConsistencyAggregator()
        
        analyses = [
            ClaimAnalysis(
                claim_id="c1",
                label=ConsistencyLabel.SUPPORTED,
                reasoning="OK"
            ),
            ClaimAnalysis(
                claim_id="c2",
                label=ConsistencyLabel.CONTRADICTED,
                reasoning="Contradicts narrative"
            ),
        ]
        
        verdict = aggregator.aggregate(analyses)
        
        assert verdict.consistency_judgment == 0

    def test_empty_analyses_is_consistent(self):
        """No analyses means trivially consistent."""
        aggregator = ConsistencyAggregator()
        
        verdict = aggregator.aggregate([])
        
        assert verdict.consistency_judgment == 1
