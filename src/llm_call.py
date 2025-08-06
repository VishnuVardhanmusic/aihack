# src/llm_call.py

import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config import MODEL_NAME, LITELLM_BASE_URL, LITELLM_API_KEY


def call_llm(prompt, max_tokens=512):
    """Send a single prompt to LiteLLM and return JSON-safe response."""
    url = f"{LITELLM_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {LITELLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    raw_output = data["choices"][0]["message"]["content"]

    return ensure_valid_json(raw_output)


def ensure_valid_json(text: str):
    """Try to ensure that the LLM response is valid JSON."""
    try:
        # First attempt: direct parse
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        # Second attempt: Extract JSON substring between first { and last }
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            candidate = text[start:end]
            return json.loads(candidate)
    except Exception:
        pass

    # If still fails, return error as dict
    return {"error": "Invalid JSON response", "raw_text": text}


def run_parallel_llm(prompts: dict):
    """Run all prompts in parallel using ThreadPoolExecutor."""
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_key = {executor.submit(call_llm, p): k for k, p in prompts.items()}

        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {"error": str(e)}

    return results
