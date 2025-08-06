import sys
import os
from src.prompt_builder import build_all_prompts
from src.llm_call import run_parallel_llm
from src.html_generated import save_responses_to_json, generate_html_from_json

def main():
    # -----------------------------
    # Step 1: Parse command-line args
    # -----------------------------
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = os.path.join("input", "data.json")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    print(f"[INFO] Using input file: {input_file}")

    # -----------------------------
    # Step 2: Build prompts
    # -----------------------------
    prompts = build_all_prompts()

    # -----------------------------
    # Step 3: Run LiteLLM calls
    # -----------------------------
    print("[INFO] Running LiteLLM calls in parallel...")
    responses = run_parallel_llm(prompts)

    # -----------------------------
    # Step 4: Derive output filenames
    # -----------------------------
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_json = os.path.join("output", f"{base_name}_report.json")
    output_html = os.path.join("output", f"{base_name}_report.html")

    # -----------------------------
    # Step 5: Save JSON + HTML
    # -----------------------------
    save_responses_to_json(responses, output_json)
    generate_html_from_json(output_json, output_html)

    print(f"[INFO] TI SCI pipeline completed successfully.")
    print(f"[INFO] JSON saved to: {output_json}")
    print(f"[INFO] HTML saved to: {output_html}")


if __name__ == "__main__":
    main()
