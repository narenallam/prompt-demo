"""
Demo: Structured Section Prompts
Demonstrates prompts using clear Markdown sections and XML structure for better organization.
"""

from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run structured sections demo."""
    print_section("Demo: Structured Section Prompts")
    
    llm = get_llm()
    print_provider_info_for_llm(llm)
    
    # Structured Example 1: Markdown Sections
    print("--- Example 1: Markdown Section Structure ---")
    markdown_sections = """# ROLE
You are an expert DevOps engineer.

# OBJECTIVE
Design a CI/CD pipeline for a Python web application.

# CONTEXT
- Application: FastAPI REST API
- Repository: GitHub
- Deployment: AWS ECS
- Testing: pytest
- Code Quality: flake8, black, mypy

# REQUIREMENTS
- Automated testing on every commit
- Code quality checks
- Security scanning
- Deployment to staging
- Manual approval for production

# OUTPUT STRUCTURE
## 1. Pipeline Overview
## 2. Stages Breakdown
## 3. Configuration Examples
## 4. Best Practices
## 5. Monitoring & Alerts"""
    
    print(f"\nPrompt:\n{markdown_sections}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(markdown_sections)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Structured Example 2: XML Structure
    print("--- Example 2: XML Structure ---")
    xml_structure = """<system>
You are a technical writer specializing in API documentation.
</system>

<task>
Write API documentation for a user authentication endpoint.
</task>

<context>
- Framework: FastAPI
- Authentication: JWT tokens
- Endpoint: POST /api/auth/login
- Request body: {username, password}
- Response: {token, user_id, expires_at}
</context>

<rules>
- Use clear, concise language
- Include request/response examples
- Document error cases
- Follow OpenAPI specification style
</rules>

<output>
1. Endpoint Overview
2. Request Format
3. Response Format
4. Error Responses
5. Code Examples
6. Authentication Flow
</output>"""
    
    print(f"\nPrompt:\n{xml_structure}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(xml_structure)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")
    
    # Structured Example 3: Hybrid Markdown/XML
    print("--- Example 3: Hybrid Structure (Markdown + XML) ---")
    hybrid_structure = """## SYSTEM
You are a data scientist.

## TASK
Analyze a dataset and provide insights.

<context>
Dataset: E-commerce sales data
Columns: date, product_id, category, price, quantity, customer_id
Time Period: Last 6 months
Records: 50,000 transactions
</context>

## ANALYSIS REQUIREMENTS
- Identify top-selling products
- Analyze sales trends
- Customer segmentation
- Revenue analysis

## OUTPUT FORMAT
### 1. Executive Summary
### 2. Data Overview
### 3. Key Findings
### 4. Visualizations (describe)
### 5. Recommendations
### 6. Next Steps"""
    
    print(f"\nPrompt:\n{hybrid_structure}")
    response, response_obj, start_time, end_time = llm.invoke_with_metadata(hybrid_structure)
    print_token_usage(response_obj, start_time, end_time)
    print(f"Response:\n{response}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

