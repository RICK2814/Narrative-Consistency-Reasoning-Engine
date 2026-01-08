"""
Stage 1: Backstory Decomposition

Transforms a backstory into atomic, falsifiable claims.
"""

from ..models import BackstoryClaim
from ..interfaces import LLMService


class BackstoryDecomposer:
    """
    Decomposes a character backstory into atomic claims.
    
    Each claim must:
    - Describe a concrete event, belief, trait, or constraint
    - Be independently verifiable against the narrative
    - Avoid vague or interpretive statements
    """

    def __init__(self, llm: LLMService):
        self.llm = llm

    def decompose(self, backstory: str) -> list[BackstoryClaim]:
        """
        Transform backstory text into a list of atomic claims.
        
        Args:
            backstory: The hypothetical character backstory text.
            
        Returns:
            List of BackstoryClaim objects, each representing a falsifiable claim.
        """
        if not backstory or not backstory.strip():
            return []
        
        claims = self.llm.decompose_backstory(backstory)
        
        # Validate claims are properly formed
        validated_claims = []
        for claim in claims:
            if claim.claim_text and claim.claim_id:
                validated_claims.append(claim)
        
        return validated_claims
