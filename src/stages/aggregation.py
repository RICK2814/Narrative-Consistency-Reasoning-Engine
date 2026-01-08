"""
Stage 4: Global Consistency Aggregation

Aggregates analysis results into a final consistency judgment.
"""

from ..models import ClaimAnalysis, FinalVerdict, ConsistencyLabel


class ConsistencyAggregator:
    """
    Aggregates claim analyses into a final verdict.
    
    Decision logic:
    - Hard rule: If ANY claim is CONTRADICTED, backstory is inconsistent (0)
    - Soft rule: If all claims are SUPPORTED or NOT_CONSTRAINED, backstory is consistent (1)
    """

    def aggregate(self, analyses: list[ClaimAnalysis]) -> FinalVerdict:
        """
        Produce final consistency judgment from claim analyses.
        
        Args:
            analyses: List of claim analysis results.
            
        Returns:
            FinalVerdict with consistency judgment and rationale.
        """
        if not analyses:
            return FinalVerdict(
                consistency_judgment=1,
                rationale="No claims to evaluate; backstory is trivially consistent.",
                claim_analyses=[]
            )
        
        # Check for any contradictions (hard rule)
        contradicted_claims = [
            a for a in analyses if a.label == ConsistencyLabel.CONTRADICTED
        ]
        
        if contradicted_claims:
            # Build rationale citing contradictions
            contradiction_details = "; ".join(
                f"'{a.claim_id}': {a.reasoning}" for a in contradicted_claims[:2]
            )
            return FinalVerdict(
                consistency_judgment=0,
                rationale=f"Backstory is inconsistent. Contradictions found: {contradiction_details}",
                claim_analyses=analyses
            )
        
        # Count support levels
        supported = sum(1 for a in analyses if a.label == ConsistencyLabel.SUPPORTED)
        weakly_constrained = sum(1 for a in analyses if a.label == ConsistencyLabel.WEAKLY_CONSTRAINED)
        not_constrained = sum(1 for a in analyses if a.label == ConsistencyLabel.NOT_CONSTRAINED)
        
        # Build summary rationale
        summary_parts = []
        if supported:
            summary_parts.append(f"{supported} claim(s) supported by evidence")
        if weakly_constrained:
            summary_parts.append(f"{weakly_constrained} claim(s) weakly constrained")
        if not_constrained:
            summary_parts.append(f"{not_constrained} claim(s) unconstrained by narrative")
        
        rationale = f"Backstory is consistent. {'; '.join(summary_parts)}."
        
        return FinalVerdict(
            consistency_judgment=1,
            rationale=rationale,
            claim_analyses=analyses
        )
