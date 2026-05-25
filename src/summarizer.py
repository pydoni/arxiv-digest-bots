"""Summarize paper abstracts using Claude Haiku."""

import json
import re

import anthropic

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You are a research paper summarizer. For each paper, you must return a JSON object with exactly these fields:

{
  "score": <integer 1-5, where 5 = highly relevant and impactful, 1 = tangential>,
  "tag": "<one of: New Method, Survey, Benchmark, Application, Framework, Analysis, Dataset, Theory>",
  "bullets": ["<bullet 1>", "<bullet 2>", "<bullet 3>"]
}

Return ONLY the JSON object, no other text."""


def summarize_papers(
    papers: list[dict],
    summary_prompt: str,
    api_key: str,
) -> list[dict]:
    client = anthropic.Anthropic(
        api_key=api_key,
        base_url="https://api.anthropic.com",
    )
    results = []

    for paper in papers:
        parsed = _summarize_one(client, paper, summary_prompt)
        results.append({**paper, **parsed})

    return results


def _summarize_one(
    client: anthropic.Anthropic,
    paper: dict,
    summary_prompt: str,
) -> dict:
    user_message = f"""{summary_prompt}

Title: {paper['title']}
Abstract: {paper['abstract']}

Respond with a JSON object containing: score (1-5), tag, and bullets (3 items)."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return _parse_response(response.content[0].text)
    except Exception as e:
        return {
            "score": 3,
            "tag": "Unknown",
            "summary": f"(Error summarizing: {e})",
        }


def _parse_response(text: str) -> dict:
    try:
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{[\s\S]*\}', text)
        if not json_match:
            return {"score": 3, "tag": "Unknown", "summary": text}

        data = json.loads(json_match.group())
        bullets = data.get("bullets", [])
        summary = "\n".join(f"\u2022 {b}" for b in bullets) if bullets else text

        return {
            "score": int(data.get("score", 3)),
            "tag": data.get("tag", "Unknown"),
            "summary": summary,
        }
    except (json.JSONDecodeError, ValueError):
        return {"score": 3, "tag": "Unknown", "summary": text}
