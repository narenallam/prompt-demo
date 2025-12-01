"""
Test Gemini API key and models using LangChain.
Demonstrates model testing, key validation, and quota monitoring.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler
import json
import urllib.request
import urllib.error

# Load environment variables
load_dotenv()


class TokenUsageCallback(BaseCallbackHandler):
    """Callback handler to capture token usage."""

    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.last_response = None

    def on_llm_end(self, response, **kwargs):
        """Capture token usage when LLM call ends."""
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            if usage:
                self.prompt_tokens = usage.get("prompt_tokens", 0)
                self.completion_tokens = usage.get("completion_tokens", 0)
                self.total_tokens = usage.get("total_tokens", 0)

        self.last_response = response


def get_api_key():
    """Get API key from environment."""
    return os.getenv("GOOGLE_API_KEY")


def list_available_models(api_key):
    """List all available Gemini models using REST API."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            result = json.loads(data)

        generative_models = []
        embedding_models = []

        for model in result.get("models", []):
            try:
                model_info = {
                    "name": model.get("name", "Unknown"),
                    "display_name": model.get("displayName", "Unknown"),
                    "supported_methods": model.get("supportedGenerationMethods", []),
                    "input_token_limit": model.get("inputTokenLimit", "N/A"),
                    "output_token_limit": model.get("outputTokenLimit", "N/A"),
                }

                if "generateContent" in model_info["supported_methods"]:
                    generative_models.append(model_info)
                elif "embedContent" in model_info["supported_methods"]:
                    embedding_models.append(model_info)
            except Exception:
                continue

        return generative_models, embedding_models
    except Exception as e:
        print(f"  Warning: Could not list models via REST API: {e}")
        # Return common models as fallback
        return [
            {"name": "models/gemini-2.5-flash", "display_name": "Gemini 2.5 Flash"},
            {"name": "models/gemini-2.5-pro", "display_name": "Gemini 2.5 Pro"},
            {"name": "models/gemini-2.0-flash", "display_name": "Gemini 2.0 Flash"},
        ], []


def test_model_with_langchain(model_name, api_key, verbose=True):
    """
    Test a specific Gemini model using LangChain.

    Args:
        model_name: Model ID (e.g., 'gemini-2.5-flash')
        api_key: Google API key
        verbose: Print detailed information

    Returns:
        dict with test results
    """
    # Clean model name (remove 'models/' prefix if present)
    clean_model_name = model_name.replace("models/", "")

    if verbose:
        print(f"\n{'' * 70}")
        print(f"Testing: {clean_model_name}")
        print(f"{'' * 70}")

    try:
        # Create callback to capture token usage
        token_callback = TokenUsageCallback()

        # Create LangChain ChatGoogleGenerativeAI instance
        llm = ChatGoogleGenerativeAI(
            model=clean_model_name,
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=100,
            callbacks=[token_callback],
        )

        # Test with a simple message
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(
                content="Say 'Hello from Gemini via LangChain!' in one sentence."
            ),
        ]

        if verbose:
            print("Sending test message...")

        response = llm.invoke(messages, config={"callbacks": [token_callback]})

        # Extract response content
        response_text = (
            response.content if hasattr(response, "content") else str(response)
        )

        # Try to get token usage from response metadata
        token_usage = {}
        if hasattr(response, "response_metadata"):
            metadata = response.response_metadata

            # Try multiple possible locations for usage data
            usage_data = None
            if "usage_metadata" in metadata:
                usage_data = metadata["usage_metadata"]
            elif "token_usage" in metadata:
                usage_data = metadata["token_usage"]

            if usage_data:
                token_usage = {
                    "prompt_tokens": usage_data.get("prompt_token_count")
                    or usage_data.get("prompt_tokens", "N/A"),
                    "completion_tokens": usage_data.get("candidates_token_count")
                    or usage_data.get("completion_tokens", "N/A"),
                    "total_tokens": usage_data.get("total_token_count")
                    or usage_data.get("total_tokens", "N/A"),
                }

        # Also check if response has usage_metadata directly
        if not token_usage and hasattr(response, "usage_metadata"):
            usage = response.usage_metadata
            token_usage = {
                "prompt_tokens": getattr(usage, "prompt_token_count", "N/A"),
                "completion_tokens": getattr(usage, "candidates_token_count", "N/A"),
                "total_tokens": getattr(usage, "total_token_count", "N/A"),
            }

        # Check callback for token usage
        if not token_usage and token_callback.total_tokens > 0:
            token_usage = {
                "prompt_tokens": token_callback.prompt_tokens,
                "completion_tokens": token_callback.completion_tokens,
                "total_tokens": token_callback.total_tokens,
            }

        if verbose:
            print(" Status: SUCCESS")
            print(f" Response: {response_text}")

            if token_usage and token_usage.get("total_tokens") != "N/A":
                print("\n Token Usage:")
                print(f"  - Prompt Tokens: {token_usage.get('prompt_tokens', 'N/A')}")
                print(
                    f"  - Completion Tokens: {token_usage.get('completion_tokens', 'N/A')}"
                )
                print(f"  - Total Tokens: {token_usage.get('total_tokens', 'N/A')}")
            else:
                print("\n Token usage info not available from this model's response")

        return {
            "success": True,
            "model": clean_model_name,
            "response": response_text,
            "token_usage": token_usage,
            "error": None,
        }

    except Exception as e:
        error_msg = str(e)

        if verbose:
            print(" Status: FAILED")
            print(f" Error: {error_msg[:150]}")

            # Provide helpful error messages
            if "429" in error_msg or "quota" in error_msg.lower():
                print("   You've exceeded your API quota. Wait or upgrade.")
            elif "403" in error_msg:
                print("   API key may be invalid or leaked.")
            elif "404" in error_msg:
                print("   Model not available for your API key.")
            elif "401" in error_msg:
                print("   Authentication failed. Check your API key.")

        return {
            "success": False,
            "model": clean_model_name,
            "response": None,
            "token_usage": None,
            "error": error_msg,
        }


def test_token_counting(model_name, api_key):
    """Test token counting capability."""
    clean_model_name = model_name.replace("models/", "")

    print(f"\n{'' * 70}")
    print(f"Testing Token Counting: {clean_model_name}")
    print(f"{'' * 70}")

    try:
        llm = ChatGoogleGenerativeAI(
            model=clean_model_name,
            google_api_key=api_key,
        )

        test_text = "Hello from Gemini via LangChain! This is a test message."

        # Use get_num_tokens method
        try:
            num_tokens = llm.get_num_tokens(test_text)
            print(f'Test text: "{test_text}"')
            print(f" Estimated tokens: {num_tokens}")
            return True
        except AttributeError:
            print("  Token counting not available via LangChain for this model")
            print(" Use the REST API version (test_gemini_key.py) for token counts")
            return False

    except Exception as e:
        print(f" Token counting failed: {str(e)[:100]}")
        return False


def test_streaming(model_name, api_key):
    """Test streaming capability with a model."""
    clean_model_name = model_name.replace("models/", "")

    print(f"\n{'' * 70}")
    print(f"Testing Streaming: {clean_model_name}")
    print(f"{'' * 70}")

    try:
        llm = ChatGoogleGenerativeAI(
            model=clean_model_name,
            google_api_key=api_key,
            temperature=0.7,
            streaming=True,
        )

        messages = [
            HumanMessage(content="Count from 1 to 5 slowly, one number per line.")
        ]

        print("Streaming response: ", end="", flush=True)

        full_response = ""
        for chunk in llm.stream(messages):
            chunk_content = chunk.content if hasattr(chunk, "content") else str(chunk)
            print(chunk_content, end="", flush=True)
            full_response += chunk_content

        print("\n Streaming test successful!")
        return True

    except Exception as e:
        print(f"\n Streaming test failed: {str(e)[:100]}")
        return False


def display_quota_info():
    """Display quota information and monitoring tips."""
    print(f"\n{'=' * 70}")
    print("QUOTA & RATE LIMITS")
    print("=" * 70)
    print("\n Google Gemini API Free Tier Limits:")
    print("  - Requests per minute (RPM): 15")
    print("  - Tokens per minute (TPM): 1,000,000")
    print("  - Requests per day (RPD): 1,500")

    print("\n Paid Tier Limits (Pay-as-you-go):")
    print("  - Requests per minute (RPM): 2,000")
    print("  - Tokens per minute (TPM): 4,000,000")

    print("\n Monitor Your Usage:")
    print("  • Google AI Studio: https://aistudio.google.com/app/apikey")
    print(
        "  • Cloud Console: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas"
    )
    print("  • Pricing: https://ai.google.dev/pricing")

    print("\n Best Practices:")
    print("  • Implement exponential backoff for rate limit errors")
    print("  • Cache responses when appropriate")
    print("  • Use batch requests for multiple queries")
    print("  • Monitor token usage to optimize costs")

    print("\n  Note on Token Usage Tracking:")
    print("  • LangChain for Gemini doesn't always return usage metadata")
    print("  • Use test_gemini_key.py (REST API) for accurate token counts")
    print("  • Or enable usage tracking in Google Cloud Console")


def main():
    """Main test function."""
    print("=" * 70)
    print("GEMINI API TEST - LANGCHAIN VERSION")
    print("=" * 70)

    # Get API key
    api_key = get_api_key()

    if not api_key:
        print("\n ERROR: GOOGLE_API_KEY not found in environment.")
        print("Please set it in your .env file or as an environment variable.")
        return

    print(f"\n API Key found: {api_key[:10]}...{api_key[-4:]}")

    # List available models
    print("\n" + "=" * 70)
    print("DISCOVERING MODELS")
    print("=" * 70)

    generative_models, embedding_models = list_available_models(api_key)

    if generative_models:
        print(f"\n Found {len(generative_models)} generative models:")
        for i, model in enumerate(generative_models, 1):
            model_id = model["name"].replace("models/", "")
            display_name = model.get("display_name", "N/A")
            input_limit = model.get("input_token_limit", "N/A")
            output_limit = model.get("output_token_limit", "N/A")

            print(f"  {i}. {model_id}")
            print(f"     Display: {display_name}")
            if input_limit != "N/A":
                print(
                    f"     Limits: {input_limit:,} input / {output_limit:,} output tokens"
                )

    if embedding_models:
        print(f"\n Found {len(embedding_models)} embedding models:")
        for model in embedding_models:
            model_id = model["name"].replace("models/", "")
            print(f"  • {model_id}")

    # Test key validity and models
    print("\n" + "=" * 70)
    print("TESTING MODELS WITH LANGCHAIN")
    print("=" * 70)

    # Select models to test (test up to 3 models)
    models_to_test = []
    if generative_models:
        for model in generative_models[:3]:
            models_to_test.append(model["name"])
    else:
        # Fallback to common models
        models_to_test = ["gemini-2.5-flash", "gemini-2.0-flash"]

    test_results = []
    successful_model = None

    for model_name in models_to_test:
        result = test_model_with_langchain(model_name, api_key, verbose=True)
        test_results.append(result)

        if result["success"] and not successful_model:
            successful_model = model_name

    # Test streaming and token counting with the first successful model
    if successful_model:
        test_streaming(successful_model, api_key)
        test_token_counting(successful_model, api_key)

    # Display quota information
    display_quota_info()

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    successful_tests = [r for r in test_results if r["success"]]
    failed_tests = [r for r in test_results if not r["success"]]

    print(f"\n Successful: {len(successful_tests)}/{len(test_results)} models")
    print(f" Failed: {len(failed_tests)}/{len(test_results)} models")

    if successful_tests:
        print("\n Working Models:")
        for result in successful_tests:
            print(f"  • {result['model']}")
            if result["token_usage"]:
                total = result["token_usage"].get("total_tokens", "N/A")
                print(f"    (Used {total} tokens)")

    if failed_tests:
        print("\n Failed Models:")
        for result in failed_tests:
            error_preview = result["error"][:80] if result["error"] else "Unknown error"
            print(f"  • {result['model']}: {error_preview}")

    # Final status
    print("\n" + "=" * 70)
    if successful_tests:
        print(" SUCCESS: Your Gemini API key is working with LangChain!")
    else:
        print(" FAILED: No models were accessible. Check your API key and quota.")
    print("=" * 70)


if __name__ == "__main__":
    main()
