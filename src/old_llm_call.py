# src/llm_call.py

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config import MODEL_NAME, LITELLM_BASE_URL, LITELLM_API_KEY

def call_llm(prompt, max_tokens=512):
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
    return data["choices"][0]["message"]["content"]

def run_parallel_llm(prompts: dict):
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_key = {executor.submit(call_llm, p): k for k, p in prompts.items()}

        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = f"Error: {str(e)}"
    return results
