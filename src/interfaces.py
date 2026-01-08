"""
LLM Interface definitions for the Narrative Consistency Reasoning Engine.
Provides an abstract base class and a mock implementation for testing.
"""

from abc import ABC, abstractmethod
from .models import BackstoryClaim, ClaimEvidence, ClaimAnalysis, EvidencePassage, ConsistencyLabel


class LLMService(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def decompose_backstory(self, backstory: str) -> list[BackstoryClaim]:
        """
        Stage 1: Transform backstory into atomic, falsifiable claims.
        Each claim must describe a concrete event, belief, trait, or constraint.
        """
        pass

    @abstractmethod
    def retrieve_evidence(
        self, narrative_text: str, claims: list[BackstoryClaim]
    ) -> list[ClaimEvidence]:
        """
        Stage 2: Locate narrative passages relevant to each claim.
        Retrieve evidence from multiple, temporally distant sections.
        """
        pass

    @abstractmethod
    def analyze_consistency(
        self, claims: list[BackstoryClaim], evidence: list[ClaimEvidence]
    ) -> list[ClaimAnalysis]:
        """
        Stage 3: Evaluate whether each claim is compatible with narrative development.
        Classify each claim as SUPPORTED, CONTRADICTED, WEAKLY_CONSTRAINED, or NOT_CONSTRAINED.
        """
        pass


class MockLLM(LLMService):
    """
    Mock LLM for testing purposes.
    Returns pre-canned responses to validate pipeline logic.
    """

    def __init__(self, force_contradiction: bool = False):
        """
        Args:
            force_contradiction: If True, one claim will be marked CONTRADICTED.
        """
        self.force_contradiction = force_contradiction

    def decompose_backstory(self, backstory: str) -> list[BackstoryClaim]:
        """Generate mock claims from backstory."""
        # Simple heuristic: split by sentences and create claims
        sentences = [s.strip() for s in backstory.split('.') if s.strip()]
        claims = []
        for i, sentence in enumerate(sentences[:5]):  # Limit to 5 claims
            claims.append(
                BackstoryClaim(
                    claim_id=f"claim_{i+1}",
                    claim_text=sentence,
                    claim_type="event" if i % 2 == 0 else "trait"
                )
            )
        return claims if claims else [
            BackstoryClaim(claim_id="claim_1", claim_text="Default claim", claim_type="event")
        ]

    def retrieve_evidence(
        self, narrative_text: str, claims: list[BackstoryClaim]
    ) -> list[ClaimEvidence]:
        """Generate mock evidence for claims."""
        evidence_list = []
        for claim in claims:
            # Create placeholder evidence from narrative
            snippet = narrative_text[:200] if len(narrative_text) > 200 else narrative_text
            evidence_list.append(
                ClaimEvidence(
                    claim_id=claim.claim_id,
                    passages=[
                        EvidencePassage(
                            passage_text=f"[Simulated evidence for: {claim.claim_text[:50]}...]",
                            location_hint="early",
                            relevance="Potentially relevant passage from narrative"
                        )
                    ]
                )
            )
        return evidence_list

    def analyze_consistency(
        self, claims: list[BackstoryClaim], evidence: list[ClaimEvidence]
    ) -> list[ClaimAnalysis]:
        """Generate mock analysis results."""
        analyses = []
        for i, claim in enumerate(claims):
            # If force_contradiction is set, mark the first claim as contradicted
            if self.force_contradiction and i == 0:
                label = ConsistencyLabel.CONTRADICTED
                reasoning = "This claim directly contradicts established narrative events."
            else:
                label = ConsistencyLabel.SUPPORTED
                reasoning = "This claim is consistent with the narrative evidence."
            
            analyses.append(
                ClaimAnalysis(
                    claim_id=claim.claim_id,
                    label=label,
                    timeline_alignment="Compatible with early narrative timeline",
                    causal_dependency="Does not break causal chain",
                    character_evolution="Consistent with character arc",
                    world_rule_constraints="Adheres to world rules",
                    reasoning=reasoning
                )
            )
        return analyses
