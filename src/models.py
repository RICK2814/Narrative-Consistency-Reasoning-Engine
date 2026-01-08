"""
Data models for the Narrative Consistency Reasoning Engine.
Uses Pydantic for validation and type safety.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ConsistencyLabel(str, Enum):
    """Classification labels for claim analysis."""
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    WEAKLY_CONSTRAINED = "WEAKLY_CONSTRAINED"
    NOT_CONSTRAINED = "NOT_CONSTRAINED"


class NarrativeInput(BaseModel):
    """Input container for narrative text and backstory."""
    narrative_text: str = Field(..., description="Full unabridged novel text")
    hypothetical_backstory: str = Field(..., description="Character backstory to validate")


class BackstoryClaim(BaseModel):
    """An atomic, falsifiable claim extracted from the backstory."""
    claim_id: str = Field(..., description="Unique identifier for the claim")
    claim_text: str = Field(..., description="The concrete claim statement")
    claim_type: str = Field(..., description="Type: event, belief, trait, or constraint")


class EvidencePassage(BaseModel):
    """A passage from the narrative relevant to a claim."""
    passage_text: str = Field(..., description="The narrative excerpt")
    location_hint: str = Field(..., description="Approximate location in narrative (early/middle/late)")
    relevance: str = Field(..., description="How this passage relates to the claim")


class ClaimEvidence(BaseModel):
    """Mapping of a claim to its supporting/contradicting evidence."""
    claim_id: str
    passages: list[EvidencePassage] = Field(default_factory=list)


class ClaimAnalysis(BaseModel):
    """Analysis result for a single claim."""
    claim_id: str
    label: ConsistencyLabel
    timeline_alignment: Optional[str] = None
    causal_dependency: Optional[str] = None
    character_evolution: Optional[str] = None
    world_rule_constraints: Optional[str] = None
    reasoning: str = Field(..., description="Brief explanation for the classification")


class FinalVerdict(BaseModel):
    """The final output of the consistency engine."""
    consistency_judgment: int = Field(..., ge=0, le=1, description="1=consistent, 0=inconsistent")
    rationale: str = Field(..., description="1-3 sentence justification with narrative citations")
    claim_analyses: list[ClaimAnalysis] = Field(default_factory=list)
