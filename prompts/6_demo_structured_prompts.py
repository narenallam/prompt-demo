"""
Demo: Structured Prompts with Templates
Demonstrates using LangChain prompt templates for structured prompts.
"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import get_llm
from demo_utils import print_provider_info_for_llm, print_token_usage
import time


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run structured prompts demo."""
    print_section("Demo: Structured Prompts with Templates")

    llm = get_llm()

    # Print provider and model information
    print_provider_info_for_llm(llm)

    model = llm.get_model()

    # Using ChatPromptTemplate
    print("--- Chat Prompt Template ---")
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that explains concepts clearly."),
            ("human", "Explain {concept} in simple terms suitable for a {audience}."),
        ]
    )

    prompt = chat_template.format_messages(
        concept="quantum computing", audience="10-year-old child"
    )
    print(f"\nSystem: {prompt[0].content}")
    print(f"Human: {prompt[1].content}")

    start_time = time.time()
    response = model.invoke(prompt)
    end_time = time.time()
    print_token_usage(response, start_time, end_time)
    print(f"Response: {response.content}\n")

    # Using PromptTemplate with output parser
    print("--- Prompt Template with Output Parser ---")
    template = PromptTemplate.from_template(
        "Generate a JSON object with the following structure for a {item_type}:\n"
        "{{\n"
        "  'name': '...',\n"
        "  'description': '...',\n"
        "  'price': '...'\n"
        "}}\n\n"
        "Item type: {item_type}"
    )

    chain = template | model | StrOutputParser()
    start_time = time.time()
    # For chains, we need to get the response differently
    # Let's invoke the model directly to get metadata
    from langchain_core.messages import HumanMessage

    prompt_msg = template.format(item_type="smartphone")
    print(f"\nPrompt: {prompt_msg}")
    model_response = model.invoke([HumanMessage(content=prompt_msg)])
    end_time = time.time()
    print_token_usage(model_response, start_time, end_time)
    result = chain.invoke({"item_type": "smartphone"})
    print(f"Response:\n{result}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure your LLM provider is properly configured and running.")
