"""
Demo: Universal Prompt Template
Demonstrates a cross-model compatible prompt template that works for all LLMs.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run universal template demo."""
    print_section("Demo: Universal Prompt Template (Cross-Model Compatible)")

    llm = get_llm()
    print_provider_info_for_llm(llm)

    # Universal Template Example 1: Technical Explanation
    print("--- Example 1: Technical Explanation ---")
    universal_prompt_1 = """# ROLE
You are an expert software engineer.

# OBJECTIVE
Explain how hash tables work in computer science.

# CONTEXT
This explanation is for computer science students learning data structures.

# RULES
- Think step-by-step
- Use structured sections
- Prefer correctness
- No hallucination

# OUTPUT
## Summary
## Explanation
## Examples
## Diagram (text-based)
## Final Answer"""

    print(f"\nPrompt:\n{universal_prompt_1}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        universal_prompt_1
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Universal Template Example 2: Creative Task
    print("--- Example 2: Creative Task ---")
    universal_prompt_2 = """# ROLE
You are a creative writing instructor.

# OBJECTIVE
Write a short story (3 paragraphs) about a robot learning to paint.

# CONTEXT
The story should be suitable for children aged 8-12.

# RULES
- Be creative and engaging
- Use vivid descriptions
- Include character development
- Keep it age-appropriate

# OUTPUT
## Story Title
## Story Content
## Moral/Lesson"""

    print(f"\nPrompt:\n{universal_prompt_2}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        universal_prompt_2
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Universal Template Example 3: Problem Solving
    print("--- Example 3: Problem Solving ---")
    universal_prompt_3 = """# ROLE
You are a data analyst.

# OBJECTIVE
Analyze the following scenario and provide recommendations:
A company's website traffic dropped 30% last month. What could be the causes?

# CONTEXT
The company is an e-commerce platform selling consumer electronics.

# RULES
- Think step-by-step
- Consider multiple factors
- Provide actionable recommendations
- Base analysis on common web analytics patterns

# OUTPUT
## Summary
## Potential Causes
## Analysis
## Recommendations
## Next Steps"""

    print(f"\nPrompt:\n{universal_prompt_3}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        universal_prompt_3
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback

        traceback.print_exc()
