"""
Demo: Advanced Parameter Combinations
Demonstrates different parameter configurations for different use cases.
"""

from llm_config import get_llm
from demo_utils import print_provider_info, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run advanced parameters demo."""
    print_section("Demo: Advanced Parameter Combinations")
    
    base_llm = get_llm()
    
    # Print base provider info
    print_provider_info()
    
    # Combination 1: Creative writing (high temperature, high top_p)
    # Note: Using higher max_tokens for Gemini to avoid empty responses
    print("--- Creative Writing Configuration ---")
    max_tokens_creative = 500  # Higher value for Gemini compatibility
    print_provider_info(temperature=1.2, top_p=0.95, max_tokens=max_tokens_creative)
    creative_llm = base_llm.update_parameters(temperature=1.2, top_p=0.95, max_tokens=max_tokens_creative)
    prompt = "Write a haiku about artificial intelligence."
    print(f"\nPrompt: {prompt}")
    try:
        response, response_obj, start_time, end_time = creative_llm.invoke_with_metadata(prompt)
        print_token_usage(response_obj, start_time, end_time)
        if response:
            print(f"\nResponse:\n{response}\n")
        else:
            print("\n(Empty response - this may occur with certain parameter combinations)\n")
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        import traceback
        traceback.print_exc()
    
    # Combination 2: Precise/Deterministic (low temperature, low top_p)
    # Note: Not setting max_tokens for Gemini as it can cause empty responses with certain combinations
    print("--- Precise/Deterministic Configuration ---")
    print_provider_info(temperature=0.1, top_p=0.3, max_tokens=None)
    precise_llm = base_llm.update_parameters(temperature=0.1, top_p=0.3, max_tokens=None)
    prompt = "List the first 5 prime numbers and explain why each is prime."
    print(f"\nPrompt: {prompt}")
    try:
        response, response_obj, start_time, end_time = precise_llm.invoke_with_metadata(prompt)
        print_token_usage(response_obj, start_time, end_time)
        if response:
            print(f"\nResponse:\n{response}\n")
        else:
            print("\n(Empty response - this may occur with certain parameter combinations)\n")
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        import traceback
        traceback.print_exc()
    
    # Combination 3: Balanced (medium parameters)
    # Note: Not setting max_tokens for Gemini as it can cause empty responses with certain combinations
    print("--- Balanced Configuration ---")
    print_provider_info(temperature=0.7, top_p=0.9, max_tokens=None)
    balanced_llm = base_llm.update_parameters(temperature=0.7, top_p=0.9, max_tokens=None)
    prompt = "Explain the difference between supervised and unsupervised learning with examples."
    print(f"\nPrompt: {prompt}")
    try:
        response, response_obj, start_time, end_time = balanced_llm.invoke_with_metadata(prompt)
        print_token_usage(response_obj, start_time, end_time)
        if response:
            print(f"\nResponse:\n{response}\n")
        else:
            print("\n(Empty response - this may occur with certain parameter combinations)\n")
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"\n❌ Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\nMake sure your LLM provider is properly configured and running.")

