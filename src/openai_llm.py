"""
OpenAI LLM implementation for the Narrative Consistency Reasoning Engine.
"""

import json
import os
from openai import OpenAI

from .models import BackstoryClaim, ClaimEvidence, ClaimAnalysis, EvidencePassage, ConsistencyLabel
from .interfaces import LLMService


class OpenAILLM(LLMService):
    """
    Real LLM implementation using OpenAI GPT.
    Requires OPENAI_API_KEY environment variable.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def _call_llm(self, prompt: str) -> str:
        """Make an API call to OpenAI."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    def decompose_backstory(self, backstory: str) -> list[BackstoryClaim]:
        """Transform backstory into atomic, falsifiable claims using OpenAI."""
        prompt = f"""You are analyzing a character backstory to extract atomic, falsifiable claims.

BACKSTORY:
{backstory}

Extract each distinct claim from this backstory. Each claim must:
- Describe a concrete event, belief, trait, or constraint
- Be independently verifiable
- Avoid vague or interpretive statements

Return a JSON array of claims with this exact format:
[
  {{"claim_id": "claim_1", "claim_text": "...", "claim_type": "event|belief|trait|constraint"}},
  ...
]

Return ONLY valid JSON, no markdown or explanations."""

        text = self._call_llm(prompt)
        
        try:
            # Remove markdown code blocks if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]
            
            claims_data = json.loads(text)
            return [BackstoryClaim(**c) for c in claims_data]
        except (json.JSONDecodeError, KeyError):
            return [BackstoryClaim(
                claim_id="claim_1",
                claim_text=backstory[:200],
                claim_type="event"
            )]

    def retrieve_evidence(
        self, narrative_text: str, claims: list[BackstoryClaim]
    ) -> list[ClaimEvidence]:
        """Find narrative passages relevant to each claim using OpenAI."""
        claims_text = "\n".join([f"- {c.claim_id}: {c.claim_text}" for c in claims])
        
        # Truncate narrative if too long
        max_narrative_len = 50000
        narrative_excerpt = narrative_text[:max_narrative_len]
        if len(narrative_text) > max_narrative_len:
            narrative_excerpt += "\n[...truncated...]"

        prompt = f"""You are finding evidence in a narrative for the following claims about a character's backstory.

CLAIMS:
{claims_text}

NARRATIVE:
{narrative_excerpt}

For each claim, find relevant passages from the narrative that either support, contradict, or constrain the claim.

Return a JSON array with this exact format:
[
  {{
    "claim_id": "claim_1",
    "passages": [
      {{"passage_text": "exact quote from narrative", "location_hint": "early|middle|late", "relevance": "supports|contradicts|constrains"}}
    ]
  }},
  ...
]

Return ONLY valid JSON, no markdown or explanations."""

        text = self._call_llm(prompt)
        
        try:
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]
            
            evidence_data = json.loads(text)
            result = []
            for ev in evidence_data:
                passages = [EvidencePassage(**p) for p in ev.get("passages", [])]
                result.append(ClaimEvidence(claim_id=ev["claim_id"], passages=passages))
            return result
        except (json.JSONDecodeError, KeyError):
            return [ClaimEvidence(claim_id=c.claim_id, passages=[]) for c in claims]

    def analyze_consistency(
        self, claims: list[BackstoryClaim], evidence: list[ClaimEvidence]
    ) -> list[ClaimAnalysis]:
        """Analyze whether each claim is consistent with narrative evidence."""
        evidence_map = {e.claim_id: e for e in evidence}
        analysis_input = []
        for claim in claims:
            ev = evidence_map.get(claim.claim_id)
            passages_text = ""
            if ev and ev.passages:
                passages_text = "\n".join([f'  - "{p.passage_text}" ({p.relevance})' for p in ev.passages])
            else:
                passages_text = "  No direct evidence found."
            
            analysis_input.append(f"CLAIM {claim.claim_id}: {claim.claim_text}\nEVIDENCE:\n{passages_text}")

        prompt = f"""Analyze whether these character backstory claims are consistent with the narrative.

{chr(10).join(analysis_input)}

For each claim, determine its consistency:
- SUPPORTED: Evidence confirms the claim
- CONTRADICTED: Evidence directly refutes the claim
- WEAKLY_CONSTRAINED: Some tension but not contradiction
- NOT_CONSTRAINED: No relevant evidence found

Return a JSON array:
[
  {{
    "claim_id": "claim_1",
    "label": "SUPPORTED|CONTRADICTED|WEAKLY_CONSTRAINED|NOT_CONSTRAINED",
    "timeline_alignment": "brief note",
    "causal_dependency": "brief note",
    "reasoning": "1-2 sentence explanation"
  }},
  ...
]

Return ONLY valid JSON."""

        text = self._call_llm(prompt)
        
        try:
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]
            
            analyses_data = json.loads(text)
            result = []
            for a in analyses_data:
                label = ConsistencyLabel(a["label"])
                result.append(ClaimAnalysis(
                    claim_id=a["claim_id"],
                    label=label,
                    timeline_alignment=a.get("timeline_alignment"),
                    causal_dependency=a.get("causal_dependency"),
                    reasoning=a.get("reasoning", "No reasoning provided")
                ))
            return result
        except (json.JSONDecodeError, KeyError, ValueError):
            return [
                ClaimAnalysis(
                    claim_id=c.claim_id,
                    label=ConsistencyLabel.NOT_CONSTRAINED,
                    reasoning="Analysis failed to parse"
                )
                for c in claims
            ]
