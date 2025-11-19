"""
Demo: Iterative Prompt Refinement
Demonstrates how to improve prompts through iteration.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run prompt iteration demo."""
    print_section("Demo: Iterative Prompt Refinement")
    
    llm = get_llm()
    
    # Print provider and model information
    print_provider_info_for_llm(llm)
    
    # Initial prompt (vague)
    print("--- Version 1: Vague Prompt ---")
    vague_prompt = "Write about Python."
    print(f"\nPrompt: {vague_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(vague_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response (first 150 chars): {response[:150]}...\n")
    
    # Improved prompt (more specific)
    print("--- Version 2: More Specific Prompt ---")
    specific_prompt = "Write a 3-paragraph explanation of Python's list comprehensions, including syntax and 2 examples."
    print(f"\nPrompt: {specific_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(specific_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Best prompt (with context and constraints)
    print("--- Version 3: Best Prompt (with context and constraints) ---")
    best_prompt = """You are a Python instructor teaching beginners.

Task: Explain Python list comprehensions.

Requirements:
- Use simple language
- Include syntax explanation
- Provide 2 practical examples
- Keep it under 200 words

Format your response as:
1. What are list comprehensions?
2. Syntax
3. Example 1
4. Example 2"""
    print(f"\nPrompt:\n{best_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(best_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")

