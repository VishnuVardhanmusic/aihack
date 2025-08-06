# main.py

from src.prompt_builder import build_all_prompts
from src.llm_call import run_parallel_llm
from src.html_generated import save_responses_to_json

def main():
    print("[INFO] Building prompts...")
    prompts = build_all_prompts()

    print("[INFO] Running LiteLLM calls in parallel...")
    responses = run_parallel_llm(prompts)

    print("[INFO] Saving responses...")
    save_responses_to_json(responses)

    print("[INFO] ChainSight AI pipeline completed successfully.")

if __name__ == "__main__":
    main()
