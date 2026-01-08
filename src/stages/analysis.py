"""
Stage 3: Temporal and Causal Constraint Analysis

Evaluates whether each claim is compatible with narrative development.
"""

from ..models import BackstoryClaim, ClaimEvidence, ClaimAnalysis
from ..interfaces import LLMService


class ConstraintAnalyzer:
    """
    Analyzes each claim against narrative constraints.
    
    Analysis dimensions:
    - Timeline alignment (early vs late events)
    - Causal dependency (does the claim enable or break later events?)
    - Character evolution consistency
    - World-rule and setting constraints
    
    Classification labels:
    - SUPPORTED: Evidence confirms the claim
    - CONTRADICTED: Evidence refutes the claim
    - WEAKLY_CONSTRAINED: Some tension but not contradiction
    - NOT_CONSTRAINED: No relevant evidence found
    """

    def __init__(self, llm: LLMService):
        self.llm = llm

    def analyze(
        self, claims: list[BackstoryClaim], evidence: list[ClaimEvidence]
    ) -> list[ClaimAnalysis]:
        """
        Evaluate each claim's compatibility with the narrative.
        
        Args:
            claims: List of backstory claims.
            evidence: Retrieved evidence for each claim.
            
        Returns:
            List of ClaimAnalysis objects with classifications.
        """
        if not claims:
            return []
        
        analyses = self.llm.analyze_consistency(claims, evidence)
        return analyses
