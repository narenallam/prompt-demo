"""
Example usage of the LLM interface system.
Demonstrates how to switch between providers easily.
"""

from llm_config import get_llm, LLMConfig, get_config


def example_basic_usage():
    """Example: Basic usage with default config."""
    print("=" * 80)
    print("Example: Basic Usage")
    print("=" * 80)

    # Get LLM from config (reads from .env or defaults)
    llm = get_llm()

    response = llm.invoke("What is artificial intelligence?")
    print(f"Response: {response}\n")


def example_switch_providers():
    """Example: Switching between providers programmatically."""
    print("=" * 80)
    print("Example: Switching Providers")
    print("=" * 80)

    # Get model names from .env config
    config = get_config()

    # Use Ollama
    print("\n--- Using Ollama ---")
    ollama_config = LLMConfig(
        provider="ollama",
        ollama_model=config.ollama_model,  # Read from .env
    )
    ollama_llm = ollama_config.create_provider()
    try:
        response = ollama_llm.invoke("Say hello in one word.")
        print(f"Ollama: {response}")
    except Exception as e:
        print(f"Ollama error: {e}")

    # Use OpenAI (if API key is set)
    print("\n--- Using OpenAI ---")
    openai_config = LLMConfig(
        provider="openai",
        openai_model=config.openai_model,  # Read from .env
        openai_api_key=None,  # Will use OPENAI_API_KEY env var if set
    )
    openai_llm = openai_config.create_provider()
    try:
        response = openai_llm.invoke("Say hello in one word.")
        print(f"OpenAI: {response}")
    except Exception as e:
        print(f"OpenAI error: {e} (API key may not be set)")

    # Use Gemini (if API key is set)
    print("\n--- Using Gemini ---")
    gemini_config = LLMConfig(
        provider="gemini",
        gemini_model=config.gemini_model,  # Read from .env
        gemini_api_key=None,  # Will use GOOGLE_API_KEY env var if set
    )
    gemini_llm = gemini_config.create_provider()
    try:
        response = gemini_llm.invoke("Say hello in one word.")
        print(f"Gemini: {response}")
    except Exception as e:
        print(f"Gemini error: {e} (API key may not be set)")


def example_parameter_tuning():
    """Example: Tuning parameters."""
    print("=" * 80)
    print("Example: Parameter Tuning")
    print("=" * 80)

    llm = get_llm()

    # Low temperature (deterministic)
    print("\n--- Low Temperature (0.1) ---")
    precise_llm = llm.update_parameters(temperature=0.1, max_tokens=100)
    response = precise_llm.invoke("List 3 colors.")
    print(response)

    # High temperature (creative)
    print("\n--- High Temperature (1.5) ---")
    creative_llm = llm.update_parameters(temperature=1.5, max_tokens=100)
    response = creative_llm.invoke("List 3 colors.")
    print(response)


def example_streaming():
    """Example: Streaming responses."""
    print("=" * 80)
    print("Example: Streaming")
    print("=" * 80)

    llm = get_llm()

    print("\nStreaming response:")
    print("-" * 80)
    for chunk in llm.stream("Count from 1 to 5, one number per line."):
        print(chunk, end="", flush=True)
    print("\n")


def example_batch():
    """Example: Batch processing."""
    print("=" * 80)
    print("Example: Batch Processing")
    print("=" * 80)

    llm = get_llm()

    prompts = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
    ]

    print("\nProcessing batch...")
    responses = llm.batch(prompts)

    for i, (prompt, response) in enumerate(zip(prompts, responses), 1):
        print(f"\n{i}. {prompt}")
        print(f"   {response[:100]}..." if len(response) > 100 else f"   {response}")


if __name__ == "__main__":
    try:
        example_basic_usage()
        example_switch_providers()
        example_parameter_tuning()
        example_streaming()
        example_batch()
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure your LLM provider is properly configured.")
