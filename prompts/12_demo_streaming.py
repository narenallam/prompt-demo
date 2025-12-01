"""
Demo: Streaming Responses
Demonstrates real-time token streaming from the LLM.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run streaming demo."""
    print_section("Demo: Streaming Responses")

    llm = get_llm()

    # Print provider and model information
    print_provider_info_for_llm(llm)

    prompt = "Write a short story about a time traveler visiting ancient Rome."
    print(f"Prompt: {prompt}\n")
    print("Streaming Response:")
    print("-" * 80)

    try:
        for chunk in llm.stream(prompt):
            print(chunk, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")


if __name__ == "__main__":
    main()
