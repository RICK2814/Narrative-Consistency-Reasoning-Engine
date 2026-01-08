"""
Main Pipeline for the Narrative Consistency Reasoning Engine.

Orchestrates the 4 stages of the reasoning pipeline.
"""

from .models import NarrativeInput, FinalVerdict
from .interfaces import LLMService
from .stages import (
    BackstoryDecomposer,
    EvidenceRetriever,
    ConstraintAnalyzer,
    ConsistencyAggregator,
)


class ConsistencyEngine:
    """
    Main entry point for the Narrative Consistency Reasoning Engine.
    
    Orchestrates the 4-stage pipeline:
    1. Backstory Decomposition
    2. Long-Context Evidence Retrieval
    3. Temporal and Causal Constraint Analysis
    4. Global Consistency Aggregation
    """

    def __init__(self, llm: LLMService):
        """
        Initialize the engine with an LLM service.
        
        Args:
            llm: An implementation of LLMService for reasoning tasks.
        """
        self.llm = llm
        self.decomposer = BackstoryDecomposer(llm)
        self.retriever = EvidenceRetriever(llm)
        self.analyzer = ConstraintAnalyzer(llm)
        self.aggregator = ConsistencyAggregator()

    def run(self, narrative_text: str, backstory: str) -> FinalVerdict:
        """
        Execute the full consistency reasoning pipeline.
        
        Args:
            narrative_text: Full unabridged novel text.
            backstory: Hypothetical character backstory to validate.
            
        Returns:
            FinalVerdict with consistency judgment (0 or 1) and rationale.
        """
        # Validate inputs
        inputs = NarrativeInput(
            narrative_text=narrative_text,
            hypothetical_backstory=backstory
        )
        
        # Stage 1: Decompose backstory into claims
        claims = self.decomposer.decompose(inputs.hypothetical_backstory)
        
        if not claims:
            return FinalVerdict(
                consistency_judgment=1,
                rationale="No falsifiable claims found in backstory; trivially consistent.",
                claim_analyses=[]
            )
        
        # Stage 2: Retrieve evidence from narrative
        evidence = self.retriever.retrieve(inputs.narrative_text, claims)
        
        # Stage 3: Analyze consistency of each claim
        analyses = self.analyzer.analyze(claims, evidence)
        
        # Stage 4: Aggregate into final verdict
        verdict = self.aggregator.aggregate(analyses)
        
        return verdict

    def run_from_input(self, narrative_input: NarrativeInput) -> FinalVerdict:
        """
        Execute pipeline from a NarrativeInput object.
        
        Args:
            narrative_input: Validated input container.
            
        Returns:
            FinalVerdict with consistency judgment and rationale.
        """
        return self.run(
            narrative_text=narrative_input.narrative_text,
            backstory=narrative_input.hypothetical_backstory
        )
