"""
Demo: Context-Grounded Prompts
Demonstrates prompts that provide rich context for better responses.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run context-grounded prompts demo."""
    print_section("Demo: Context-Grounded Prompts")

    llm = get_llm()
    print_provider_info_for_llm(llm)

    # Context Example 1: Technical Context
    print("--- Example 1: Technical Context ---")
    technical_context = """## SYSTEM
You are a senior software engineer reviewing code.

## CONTEXT
The team is working on a microservices architecture using:
- Python 3.11
- FastAPI framework
- PostgreSQL database
- Docker containers
- Kubernetes orchestration

The codebase follows these patterns:
- Repository pattern for data access
- Dependency injection for services
- Async/await for I/O operations
- Type hints throughout

## TASK
Review this code snippet and suggest improvements:

```python
def get_user(user_id: int):
    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

## OUTPUT FORMAT
1. Issues Found
2. Suggested Improvements
3. Refactored Code
4. Best Practices Applied"""

    print(f"\nPrompt:\n{technical_context}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        technical_context
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Context Example 2: Business Context
    print("--- Example 2: Business Context ---")
    business_context = """## SYSTEM
You are a business analyst.

## CONTEXT
Company: TechStart Inc. (B2B SaaS platform)
Industry: Project management software
Current Situation:
- 50 employees
- $5M ARR (Annual Recurring Revenue)
- Growing 20% month-over-month
- Primary customers: Small to medium businesses (10-100 employees)
- Main competitors: Asana, Monday.com, Trello

Challenge: Customer churn rate increased from 5% to 12% in last quarter.

## TASK
Analyze potential causes and recommend strategies to reduce churn.

## OUTPUT FORMAT
1. Root Cause Analysis
2. Impact Assessment
3. Recommended Strategies
4. Implementation Priority
5. Success Metrics"""

    print(f"\nPrompt:\n{business_context}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        business_context
    )
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")

    # Context Example 3: Educational Context
    print("--- Example 3: Educational Context ---")
    educational_context = """## SYSTEM
You are a computer science professor.

## CONTEXT
Course: Introduction to Algorithms (CS 101)
Students: First-year computer science students
Prerequisites: Basic programming in Python
Learning Objectives:
- Understand time complexity
- Analyze algorithm efficiency
- Compare different approaches

Previous Topics Covered:
- Arrays and linked lists
- Basic sorting algorithms (bubble sort, selection sort)
- Recursion basics

## TASK
Explain merge sort algorithm in a way that builds on their existing knowledge.

## OUTPUT FORMAT
1. Connection to Previous Topics
2. Algorithm Explanation
3. Step-by-Step Example
4. Time Complexity Analysis
5. Comparison with Previous Algorithms
6. Practice Exercise"""

    print(f"\nPrompt:\n{educational_context}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(
        educational_context
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
