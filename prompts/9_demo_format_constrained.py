"""
Demo: Format-Constrained Prompts
Demonstrates prompts that request specific output formats:
- Tables
- Code blocks
- Structured lists
- JSON
- Step-by-step procedures
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run format-constrained prompts demo."""
    print_section("Demo: Format-Constrained Prompts")
    
    llm = get_llm()
    print_provider_info_for_llm(llm)
    
    # Format 1: Table Output
    print("--- Format 1: Table Output ---")
    table_prompt = """Compare Python, JavaScript, and Java programming languages.

Present the comparison in a table format with columns:
- Language Name
- Typing (Static/Dynamic)
- Use Cases
- Learning Curve

Format as a markdown table."""
    
    print(f"\nPrompt:\n{table_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(table_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Format 2: Code Block
    print("--- Format 2: Code Block Output ---")
    code_prompt = """Write a Python function to calculate the factorial of a number.

Requirements:
- Include type hints
- Add docstring
- Handle edge cases (0, negative numbers)
- Include example usage

Format the code in a code block with proper syntax highlighting."""
    
    print(f"\nPrompt:\n{code_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(code_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Format 3: Structured List
    print("--- Format 3: Structured List ---")
    list_prompt = """List the steps to deploy a web application to production.

Format as a numbered list with:
1. Each step clearly numbered
2. Sub-bullets for details
3. Brief explanations for each step

Structure:
Step 1: [Title]
  - Detail 1
  - Detail 2
  Explanation: ...
"""
    
    print(f"\nPrompt:\n{list_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(list_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Format 4: JSON Output
    print("--- Format 4: JSON Output ---")
    json_prompt = """Create a JSON object representing a user profile.

Include the following fields:
- name (string)
- age (number)
- email (string)
- skills (array of strings)
- preferences (object with theme and notifications)

Output only valid JSON, no additional text."""
    
    print(f"\nPrompt:\n{json_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(json_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Format 5: Step-by-Step Procedure
    print("--- Format 5: Step-by-Step Procedure ---")
    procedure_prompt = """Explain how to troubleshoot a slow database query.

Format as a step-by-step procedure:
1. Each step should be clearly numbered
2. Include "What to check" and "How to fix" for each step
3. Use clear headings
4. End with a summary

Structure:
## Step 1: [Title]
**What to check:** ...
**How to fix:** ...

## Step 2: [Title]
...
"""
    
    print(f"\nPrompt:\n{procedure_prompt}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(procedure_prompt)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

