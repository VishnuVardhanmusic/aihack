# src/html_generated.py

import json
import os

OUTPUT_FILE = os.path.join("output", "chainsight_report.json")

def save_responses_to_json(responses: dict):
    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"ChainSight_AI_Report": responses}, f, indent=4)
    print(f"[INFO] Report saved to {OUTPUT_FILE}")
