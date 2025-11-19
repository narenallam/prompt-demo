"""
Demo: Basic LLM Invoke
Demonstrates simple prompt invocation with the configured LLM provider.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run basic invoke demo."""
    print_section("Demo: Basic LLM Invoke")
    
    # Get LLM provider from configuration (uses PROVIDER from .env)
    llm = get_llm()
    
    # Print provider and model information
    print_provider_info_for_llm(llm)
    
    # Simple prompt
    prompt = "Explain what machine learning is in one paragraph."
    print(f"\nPrompt: {prompt}")
    
    try:
        response, response_obj, start_time, end_time = llm.invoke_with_metadata(prompt)
        print_token_usage(response_obj, start_time, end_time)
        print(f"\nResponse:\n{response}\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")


if __name__ == "__main__":
    main()

