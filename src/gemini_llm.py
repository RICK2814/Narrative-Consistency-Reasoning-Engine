"""
Gemini LLM implementation using google-generativeai SDK.
"""

import json
import os
import time
import google.generativeai as genai

from .models import BackstoryClaim, ClaimEvidence, ClaimAnalysis, EvidencePassage, ConsistencyLabel
from .interfaces import LLMService


class GeminiLLM(LLMService):
    """
    Real LLM implementation using Google Gemini.
    Requires GEMINI_API_KEY environment variable.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.max_retries = 3
        self.retry_delay = 35

    def _call_with_retry(self, prompt: str) -> str:
        """Make API call with retry on rate limit."""
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                err_str = str(e).lower()
                if "429" in str(e) or "quota" in err_str or "rate" in err_str or "resource" in err_str:
                    if attempt < self.max_retries - 1:
                        print(f"Rate limited, waiting {self.retry_delay}s... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                    else:
                        raise
                else:
                    raise

    def decompose_backstory(self, backstory: str) -> list[BackstoryClaim]:
        """Transform backstory into atomic, falsifiable claims."""
        prompt = f"""Extract atomic claims from this backstory. Each claim must be concrete and verifiable.

BACKSTORY:
{backstory}

Return JSON array:
[{{"claim_id": "claim_1", "claim_text": "...", "claim_type": "event|belief|trait|constraint"}}]

Return ONLY valid JSON."""

        try:
            text = self._call_with_retry(prompt).strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            
            claims_data = json.loads(text)
            return [BackstoryClaim(**c) for c in claims_data]
        except Exception:
            return [BackstoryClaim(claim_id="claim_1", claim_text=backstory[:200], claim_type="event")]

    def retrieve_evidence(self, narrative_text: str, claims: list[BackstoryClaim]) -> list[ClaimEvidence]:
        """Find narrative passages relevant to each claim."""
        claims_text = "\n".join([f"- {c.claim_id}: {c.claim_text}" for c in claims])
        narrative_excerpt = narrative_text[:30000]

        prompt = f"""Find evidence for these claims:

CLAIMS:
{claims_text}

NARRATIVE:
{narrative_excerpt}

Return JSON:
[{{"claim_id": "claim_1", "passages": [{{"passage_text": "quote", "location_hint": "early|middle|late", "relevance": "supports|contradicts|constrains"}}]}}]

Return ONLY valid JSON."""

        try:
            text = self._call_with_retry(prompt).strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            
            evidence_data = json.loads(text)
            return [ClaimEvidence(claim_id=ev["claim_id"], passages=[EvidencePassage(**p) for p in ev.get("passages", [])]) for ev in evidence_data]
        except Exception:
            return [ClaimEvidence(claim_id=c.claim_id, passages=[]) for c in claims]

    def analyze_consistency(self, claims: list[BackstoryClaim], evidence: list[ClaimEvidence]) -> list[ClaimAnalysis]:
        """Analyze whether each claim is consistent with narrative evidence."""
        evidence_map = {e.claim_id: e for e in evidence}
        analysis_input = []
        for claim in claims:
            ev = evidence_map.get(claim.claim_id)
            passages_text = "\n".join([f'  - "{p.passage_text}" ({p.relevance})' for p in ev.passages]) if ev and ev.passages else "  No evidence."
            analysis_input.append(f"CLAIM {claim.claim_id}: {claim.claim_text}\nEVIDENCE:\n{passages_text}")

        prompt = f"""Classify these claims:

{chr(10).join(analysis_input)}

Labels: SUPPORTED, CONTRADICTED, WEAKLY_CONSTRAINED, NOT_CONSTRAINED

Return JSON:
[{{"claim_id": "claim_1", "label": "SUPPORTED", "reasoning": "explanation"}}]

Return ONLY valid JSON."""

        try:
            text = self._call_with_retry(prompt).strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            
            analyses_data = json.loads(text)
            return [ClaimAnalysis(claim_id=a["claim_id"], label=ConsistencyLabel(a["label"]), reasoning=a.get("reasoning", "")) for a in analyses_data]
        except Exception:
            return [ClaimAnalysis(claim_id=c.claim_id, label=ConsistencyLabel.NOT_CONSTRAINED, reasoning="Analysis failed") for c in claims]
