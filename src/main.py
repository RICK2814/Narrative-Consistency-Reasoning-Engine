"""
Entry point for the Narrative Consistency Reasoning Engine.

Usage:
    python -m src.main --narrative path/to/narrative.txt --backstory path/to/backstory.txt
"""

import argparse
import json
import os
import sys
from pathlib import Path

from .pipeline import ConsistencyEngine
from .interfaces import MockLLM


def main():
    parser = argparse.ArgumentParser(
        description="Narrative Consistency Reasoning Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.main --narrative novel.txt --backstory backstory.txt
    python -m src.main --narrative novel.txt --backstory backstory.txt --output result.json
    python -m src.main --narrative novel.txt --backstory backstory.txt --mock
        """
    )
    parser.add_argument(
        "--narrative", "-n",
        type=Path,
        required=True,
        help="Path to the narrative text file"
    )
    parser.add_argument(
        "--backstory", "-b",
        type=Path,
        required=True,
        help="Path to the backstory text file"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output JSON file (default: stdout)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force use of mock LLM instead of Gemini"
    )
    
    args = parser.parse_args()
    
    # Read input files
    try:
        narrative_text = args.narrative.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: Narrative file not found: {args.narrative}", file=sys.stderr)
        sys.exit(1)
    
    try:
        backstory_text = args.backstory.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: Backstory file not found: {args.backstory}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize LLM - check for API keys in order: OpenAI, Gemini, then Mock
    if args.mock:
        print("Using Mock LLM...", file=sys.stderr)
        llm = MockLLM()
    elif os.environ.get("OPENAI_API_KEY"):
        from .openai_llm import OpenAILLM
        print("Using OpenAI LLM...", file=sys.stderr)
        llm = OpenAILLM()
    elif os.environ.get("GEMINI_API_KEY"):
        from .gemini_llm import GeminiLLM
        print("Using Gemini LLM...", file=sys.stderr)
        llm = GeminiLLM()
    else:
        print("No API key found. Set OPENAI_API_KEY or GEMINI_API_KEY. Using Mock LLM.", file=sys.stderr)
        llm = MockLLM()
    
    engine = ConsistencyEngine(llm=llm)
    
    # Run pipeline
    verdict = engine.run(narrative_text=narrative_text, backstory=backstory_text)
    
    # Output result
    result = {
        "consistency_judgment": verdict.consistency_judgment,
        "rationale": verdict.rationale,
        "claim_analyses": [
            {
                "claim_id": a.claim_id,
                "label": a.label.value,
                "reasoning": a.reasoning
            }
            for a in verdict.claim_analyses
        ]
    }
    
    output_json = json.dumps(result, indent=2)
    
    if args.output:
        args.output.write_text(output_json, encoding="utf-8")
        print(f"Result written to: {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
