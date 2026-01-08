"""
Stage 2: Long-Context Evidence Retrieval

Locates narrative passages relevant to each backstory claim.
"""

from ..models import BackstoryClaim, ClaimEvidence
from ..interfaces import LLMService


class EvidenceRetriever:
    """
    Retrieves evidence from the narrative for each claim.
    
    Prioritizes:
    - Evidence from multiple, temporally distant sections
    - Passages establishing constraints, commitments, or irreversible events
    - Both supporting and contradicting evidence
    """

    def __init__(self, llm: LLMService):
        self.llm = llm

    def retrieve(
        self, narrative_text: str, claims: list[BackstoryClaim]
    ) -> list[ClaimEvidence]:
        """
        Find narrative passages relevant to each claim.
        
        Args:
            narrative_text: The full narrative text to search.
            claims: List of claims to find evidence for.
            
        Returns:
            List of ClaimEvidence objects mapping claims to passages.
        """
        if not narrative_text or not claims:
            return []
        
        evidence = self.llm.retrieve_evidence(narrative_text, claims)
        return evidence
