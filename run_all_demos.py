"""
Run all prompt engineering demos in sequence.
"""

import sys
from llm_config import get_config, get_llm


def print_header():
    """Print demo header."""
    config = get_config()
    # Get model name based on provider
    if config.provider == "ollama":
        model_name = config.ollama_model
    elif config.provider == "openai":
        model_name = config.openai_model
    elif config.provider == "gemini":
        model_name = config.gemini_model
    else:
        model_name = "unknown"

    print("\n" + "=" * 80)
    print("  PROMPT ENGINEERING DEMOS")
    print(f"  Provider: {config.provider.upper()}")
    print(f"  Model: {model_name}")
    print("  Framework: LangChain")
    print("=" * 80)


def test_connection():
    """Test LLM connection."""
    print("\nTesting connection to LLM provider...")
    try:
        llm = get_llm()
        test_response = llm.invoke("Say 'Hello' in one word.")
        print(f" Connection successful! Model responded: {test_response}\n")
        return True
    except Exception as e:
        print(f" Connection failed: {e}\n")
        return False


def run_demo(module_name: str):
    """Run a demo module."""
    try:
        print(f"\n{'=' * 80}")
        print(f"Running {module_name}...")
        print("=" * 80)

        # Import and run the demo
        module = __import__(module_name)
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Warning: {module_name} does not have a main() function")
    except Exception as e:
        print(f" Error running {module_name}: {e}")


def main():
    """Run all demos."""
    print_header()

    if not test_connection():
        print("\nPlease check your configuration:")
        config = get_config()
        if config.provider == "ollama":
            print("1. Ollama is running (ollama serve)")
            print(f"2. Model '{config.ollama_model}' is installed")
            print(f"3. Ollama API is accessible at {config.ollama_base_url}")
        elif config.provider == "openai":
            print("1. OPENAI_API_KEY is set in environment or config")
            print(f"2. Model '{config.openai_model}' is available")
        elif config.provider == "gemini":
            print("1. GOOGLE_API_KEY is set in environment or config")
            print(f"2. Model '{config.gemini_model}' is available")
        sys.exit(1)

    # List of demos to run (in teaching order)
    demos = [
        "1_demo_basic_invoke",
        "2_demo_parameter_tuning",
        "3_demo_advanced_parameters",
        "4_demo_prompt_techniques",
        "5_demo_prompt_iteration",
        "6_demo_structured_prompts",
        "7_demo_model_specific_templates",
        "8_demo_universal_template",
        "9_demo_format_constrained",
        "10_demo_context_grounded",
        "11_demo_structured_sections",
        "12_demo_streaming",
    ]

    for demo in demos:
        run_demo(demo)

    print("\n" + "=" * 80)
    print("  ALL DEMOS COMPLETED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
