"""
Demo: Prompt Engineering Techniques
Demonstrates zero-shot, few-shot, chain-of-thought, and role-based prompting.
"""

from langchain_core.messages import SystemMessage, HumanMessage
from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run prompt engineering techniques demo."""
    print_section("Demo: Prompt Engineering Techniques")
    
    llm = get_llm()
    
    # Print provider and model information
    print_provider_info_for_llm(llm)
    
    # Technique 1: Zero-shot prompting
    print("--- Zero-Shot Prompting ---")
    zero_shot = "Classify the sentiment of this text: 'I love this new product!'"
    print(f"\nPrompt: {zero_shot}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(zero_shot)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response: {response}\n")
    
    # Technique 2: Few-shot prompting
    print("--- Few-Shot Prompting ---")
    few_shot = """Translate the following English words to French:

English: hello
French: bonjour

English: goodbye
French: au revoir

English: thank you
French:"""
    print(f"\nPrompt:\n{few_shot}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(few_shot)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response: {response}\n")
    
    # Technique 3: Chain-of-thought prompting
    print("--- Chain-of-Thought Prompting ---")
    cot_prompt = """Solve this math problem step by step:

Question: A store has 15 apples. They sell 6 apples in the morning and 4 apples in the afternoon. How many apples are left?

Let's think step by step:"""
    print(f"\nPrompt:\n{cot_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(cot_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response: {response}\n")
    
    # Technique 4: Role-based prompting
    print("--- Role-Based Prompting ---")
    role_prompt = [
        SystemMessage(content="You are an expert Python programmer with 20 years of experience."),
        HumanMessage(content="Write a Python function to check if a number is prime. Include docstring and type hints.")
    ]
    print("\nSystem: You are an expert Python programmer with 20 years of experience.")
    print("User: Write a Python function to check if a number is prime. Include docstring and type hints.")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(role_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")

