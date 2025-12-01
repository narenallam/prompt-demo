"""
Demo: Model-Specific Prompt Templates
Demonstrates optimal prompt formats for different LLM models:
- Markdown for ChatGPT/Gemini
- XML for Claude
- Structured sections for all models
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run model-specific templates demo."""
    print_section("Demo: Model-Specific Prompt Templates")

    llm = get_llm()
    print_provider_info_for_llm(llm)

    # Template 1: Markdown Format (Optimal for ChatGPT/Gemini)
    print("--- Template 1: Markdown Format (ChatGPT/Gemini Style) ---")
    markdown_prompt = """## SYSTEM
You are an expert Python instructor.

## TASK
Explain Python decorators with examples.

## GUIDELINES
- Think step-by-step
- Use clean structure
- Include code examples
- No hallucinations

## OUTPUT FORMAT
1. Summary
2. Explanation
3. Code Examples
4. Use Cases
5. Final Answer"""

    print(f"\nPrompt:\n{markdown_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        markdown_prompt
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Template 2: XML Format (Optimal for Claude, but works with others)
    print("--- Template 2: XML Format (Claude Style) ---")
    xml_prompt = """<system>You are an expert data scientist.</system>
<task>Explain the difference between supervised and unsupervised learning.</task>
<context>This is for students learning machine learning basics.</context>
<rules>
- Think step-by-step
- Follow structure exactly
- Use examples
- No hallucination
</rules>
<output>
1. Summary
2. Explanation
3. Examples
4. Comparison Table
5. Final Answer
</output>"""

    print(f"\nPrompt:\n{xml_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(xml_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Template 3: Gemini-Specific Format
    print("--- Template 3: Gemini-Specific Format ---")
    gemini_prompt = """# Instruction
You are a world-class software architect.

# Task
Design a REST API for a todo application.

# Context
The API should support CRUD operations and user authentication.

# Reasoning Rules
- Be clear, structured, precise
- Use headings & bullets
- Include request/response examples

# Output
- Summary
- API Endpoints
- Request Examples
- Response Examples
- Final Design"""

    print(f"\nPrompt:\n{gemini_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        gemini_prompt
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Template 4: DeepSeek-Style (Step-by-step reasoning)
    print("--- Template 4: DeepSeek-Style (Step-by-Step Reasoning) ---")
    deepseek_prompt = """## SYSTEM
You are DeepSeek, an expert mathematician with strong reasoning.

## TASK
Solve: A store has 20 apples. They sell 8 in the morning and 5 in the afternoon. 
How many apples are left?

## CONTEXT
This is a word problem for elementary students.

## REASONING RULES
- Think step-by-step with clarity
- Show your work
- Prioritize correctness
- No hallucinations

## OUTPUT FORMAT
1. Summary
2. Reasoning Steps
3. Calculation
4. Final Answer"""

    print(f"\nPrompt:\n{deepseek_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        deepseek_prompt
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
