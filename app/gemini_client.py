from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import requests

@dataclass(frozen=True)
class GeminiConfig:
    # Minimal configuration for the Gemini API call.
    api_key: str
    model: str = "gemini-2.5-flash"

class GeminiError(RuntimeError):
    pass

def _parse_response(data: dict[str, Any]) -> str:
    # Extract the first text chunk from the model response.
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise GeminiError("Unexpected Gemini response format.") from exc


def generate_commit(config: GeminiConfig, prompt: str) -> dict[str, str]:
    # Call Gemini and parse the JSON response with prefix/message.
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{config.model}:generateContent?key={config.api_key}"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {"temperature": 0.2},
    }
    response = requests.post(url, json=payload, timeout=60)
    if not response.ok:
        raise GeminiError(f"Gemini request failed: {response.status_code} {response.text}")

    text = _parse_response(response.json()).strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise GeminiError(f"Failed to parse JSON: {text}") from exc
