"""
Demo: Parameter Tuning
Demonstrates how different parameters (temperature, top_p, max_tokens) affect responses.
"""

from llm_config import get_llm
from demo_utils import print_provider_info, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run parameter tuning demo."""
    print_section("Demo: Parameter Tuning")

    # Print base provider info
    print_provider_info()

    base_prompt = "Write a creative story about a robot learning to paint."

    # Test different temperatures
    print("--- Temperature Comparison ---")
    temperatures = [0.1, 0.7, 1.5]

    llm = get_llm()

    for temp in temperatures:
        print(f"\nTemperature: {temp}")
        print_provider_info(temperature=temp, max_tokens=100)
        llm_temp = llm.update_parameters(temperature=temp, max_tokens=100)
        response, response_obj, start_time, end_time = llm_temp.invoke_with_metadata(
            base_prompt
        )
        print_token_usage(response_obj, start_time, end_time)
        if response:
            print(response[:200] + "..." if len(response) > 200 else response + "\n")
        else:
            print("(Empty response)\n")

    # Test top_p parameter
    print("\n\n--- Top-p Comparison ---")
    top_p_values = [0.1, 0.9]

    for top_p in top_p_values:
        print(f"\nTop-p: {top_p}")
        print_provider_info(temperature=0.7, top_p=top_p, max_tokens=100)
        llm_top_p = llm.update_parameters(temperature=0.7, top_p=top_p, max_tokens=100)
        response, response_obj, start_time, end_time = llm_top_p.invoke_with_metadata(
            "Generate a list of 5 creative product names for a tech startup."
        )
        print_token_usage(response_obj, start_time, end_time)
        if response:
            print(response[:200] + "..." if len(response) > 200 else response + "\n")
        else:
            print("(Empty response)\n")

    # Test max_tokens
    print("\n\n--- Max Tokens Comparison ---")
    token_limits = [50, 200]

    for max_tokens in token_limits:
        print(f"\nMax Tokens: {max_tokens}")
        print_provider_info(temperature=0.7, max_tokens=max_tokens)
        llm_tokens = llm.update_parameters(temperature=0.7, max_tokens=max_tokens)
        response, response_obj, start_time, end_time = llm_tokens.invoke_with_metadata(
            "Explain the concept of recursion in programming."
        )
        print_token_usage(response_obj, start_time, end_time)
        print(response + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")
