"""
Test Gemini API key and list available models using only Python standard library.
No external dependencies required - uses urllib instead of requests.
"""

import os
import json
import urllib.request
import urllib.error


def get_api_key():
    """Get API key from .env file or environment."""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        # Try to read from .env file manually
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        # Remove quotes if present
                        api_key = api_key.strip('"').strip("'")
                        break
        except FileNotFoundError:
            pass

    return api_key


def extract_quota_info(headers):
    """Extract quota and rate limit information from response headers."""
    quota_info = {}

    # Common header names for rate limiting
    rate_limit_headers = {
        "X-RateLimit-Limit": "Rate Limit",
        "X-RateLimit-Remaining": "Remaining Requests",
        "X-RateLimit-Reset": "Reset Time",
        "X-Quota-Limit": "Quota Limit",
        "X-Quota-Remaining": "Quota Remaining",
        "X-Daily-Quota-Limit": "Daily Quota Limit",
        "X-Daily-Quota-Remaining": "Daily Quota Remaining",
    }

    for header_name, display_name in rate_limit_headers.items():
        if header_name in headers or header_name.lower() in headers:
            value = headers.get(header_name) or headers.get(header_name.lower())
            quota_info[display_name] = value

    return quota_info


def check_quota_via_api(api_key):
    """
    Try to get quota information from Google Cloud API.
    Note: This requires the API key to have access to Cloud APIs.
    """
    # Check if we can get project info
    try:
        # Try to get quota info from the generativelanguage API
        url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.headers)
            return extract_quota_info(headers)
    except Exception:
        return {}


def display_quota_info(headers_dict):
    """Display quota information from headers."""
    quota_info = extract_quota_info(headers_dict)

    if quota_info:
        print("\n" + "=" * 70)
        print("QUOTA & RATE LIMIT INFORMATION")
        print("=" * 70)
        for key, value in quota_info.items():
            print(f"  {key}: {value}")
        return True
    return False


def list_models(api_key):
    """List all available Gemini models."""
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            headers = dict(response.headers)
            result = json.loads(data)
            result["_headers"] = headers  # Store headers for quota info
            return result
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def test_generation(api_key, model_name):
    """Test text generation with a specific model."""
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {"parts": [{"text": "Say 'Hello from Gemini!' in one sentence."}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 100,
        },
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result_data = response.read()
            headers = dict(response.headers)
            result = json.loads(result_data)
            result["_headers"] = headers  # Store headers for quota info
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {
            "error": f"HTTP {e.code}: {e.reason}",
            "status_code": e.code,
            "details": error_body[:200],
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    """Main test function."""
    print("=" * 70)
    print("GEMINI API KEY TEST (Using REST API - Standard Library Only)")
    print("=" * 70)

    # Get API key
    api_key = get_api_key()

    if not api_key:
        print("\n ERROR: GOOGLE_API_KEY not found.")
        print("Please set it in your .env file or environment variables.")
        return

    print(f"\n API Key found: {api_key[:10]}...{api_key[-4:]}")

    # List available models
    print("\n" + "=" * 70)
    print("LISTING AVAILABLE MODELS")
    print("=" * 70)

    models_data = list_models(api_key)

    if "error" in models_data:
        print(f"\n Error listing models: {models_data['error']}")
        if "401" in str(models_data.get("error", "")):
            print(" Your API key may be invalid.")
        elif "403" in str(models_data.get("error", "")):
            print(" Your API key may not have permission to access the API.")
        return

    if "models" not in models_data:
        print("\n No models found in API response")
        print(f"Response: {json.dumps(models_data, indent=2)}")
        return

    # Check for quota information in response headers
    if "_headers" in models_data:
        has_quota = display_quota_info(models_data["_headers"])
        if not has_quota:
            # If no quota info in headers, show where to check
            print("\n" + "=" * 70)
            print("QUOTA INFORMATION")
            print("=" * 70)
            print("  ℹ  Quota details are not available in API response headers.")
            print("   To check your quota and usage:")
            print("      1. Visit: https://aistudio.google.com/app/apikey")
            print(
                "      2. Or: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas"
            )
            print(
                "      3. View quotas in Google Cloud Console > APIs & Services > Quotas"
            )

    # Categorize models
    generative_models = []
    embedding_models = []
    other_models = []

    for model in models_data.get("models", []):
        supported_methods = model.get("supportedGenerationMethods", [])

        if "generateContent" in supported_methods:
            generative_models.append(model)
        elif "embedContent" in supported_methods:
            embedding_models.append(model)
        else:
            other_models.append(model)

    # Display generative models
    if generative_models:
        print(f"\n GENERATIVE MODELS ({len(generative_models)}):")
        print("-" * 70)
        for model in generative_models:
            print(f"\n  Model ID: {model.get('name', 'N/A')}")
            print(f"  Display Name: {model.get('displayName', 'N/A')}")
            desc = model.get("description", "N/A")
            if len(desc) > 100:
                desc = desc[:97] + "..."
            print(f"  Description: {desc}")
            print(f"  Input Token Limit: {model.get('inputTokenLimit', 'N/A')}")
            print(f"  Output Token Limit: {model.get('outputTokenLimit', 'N/A')}")
            print(
                f"  Supported Methods: {', '.join(model.get('supportedGenerationMethods', []))}"
            )

    # Display embedding models
    if embedding_models:
        print(f"\n\n EMBEDDING MODELS ({len(embedding_models)}):")
        print("-" * 70)
        for model in embedding_models:
            print(f"\n  Model ID: {model.get('name', 'N/A')}")
            print(f"  Display Name: {model.get('displayName', 'N/A')}")
            print(
                f"  Supported Methods: {', '.join(model.get('supportedGenerationMethods', []))}"
            )

    # Display other models
    if other_models:
        print(f"\n\n OTHER MODELS ({len(other_models)}):")
        print("-" * 70)
        for model in other_models:
            print(f"\n  Model ID: {model.get('name', 'N/A')}")
            print(f"  Display Name: {model.get('displayName', 'N/A')}")
            print(
                f"  Supported Methods: {', '.join(model.get('supportedGenerationMethods', []))}"
            )

    # Test generation with available models
    print("\n" + "=" * 70)
    print("CONNECTION TEST")
    print("=" * 70)
    print("\nTesting text generation...")

    if not generative_models:
        print("\n  No generative models available to test.")
        return

    # Try the first few available generative models
    success = False
    for model in generative_models[:3]:  # Try up to 3 models
        model_id = model.get("name", "").replace("models/", "")

        if not model_id:
            continue

        print(f"\nAttempting with model: {model_id}...")

        result = test_generation(api_key, model_id)

        if "error" in result:
            error_msg = result["error"]
            status_code = result.get("status_code", "N/A")
            print(f"  Failed (Status: {status_code}): {error_msg[:100]}")

            if result.get("details"):
                print(f"   Details: {result['details']}")

            if "quota" in str(error_msg).lower() or "429" in str(status_code):
                print("    You may have exceeded your API quota.")
            elif "404" in str(status_code):
                print("    Model not available.")
            continue

        # Extract the generated text
        try:
            generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"\n Model: {model_id}")
            print(f" Response: {generated_text}")

            # Check for usage metadata in response
            if "usageMetadata" in result:
                usage = result["usageMetadata"]
                print("\n Token Usage for this request:")
                if "promptTokenCount" in usage:
                    print(f"  - Prompt Tokens: {usage['promptTokenCount']}")
                if "candidatesTokenCount" in usage:
                    print(f"  - Response Tokens: {usage['candidatesTokenCount']}")
                if "totalTokenCount" in usage:
                    print(f"  - Total Tokens: {usage['totalTokenCount']}")

            # Check headers for quota info
            if "_headers" in result:
                quota_info = extract_quota_info(result["_headers"])
                if quota_info:
                    print("\n Rate Limit Info:")
                    for key, value in quota_info.items():
                        print(f"  - {key}: {value}")

            print("\n" + "=" * 70)
            print(" SUCCESS: Gemini API key is working correctly!")
            print("=" * 70)
            success = True
            break
        except (KeyError, IndexError) as e:
            print(f"  Unexpected response format: {e}")
            print(f"   Response: {json.dumps(result, indent=2)[:300]}")
            continue

    if not success:
        print("\n All test models failed.")
        print("Your API key may not have access to any models or quota is exceeded.")

    print(f"\n\n{'=' * 70}")
    print("SUMMARY")
    print("=" * 70)
    print(f"Total models found: {len(models_data.get('models', []))}")
    print(f"  - Generative: {len(generative_models)}")
    print(f"  - Embedding: {len(embedding_models)}")
    print(f"  - Other: {len(other_models)}")

    print(f"\n{'=' * 70}")
    print("QUOTA MONITORING")
    print("=" * 70)
    print(" To monitor your API quota and usage in detail:")
    print("\n  Free Tier Limits (as of 2024):")
    print("    - 15 requests per minute (RPM)")
    print("    - 1 million tokens per minute (TPM)")
    print("    - 1,500 requests per day (RPD)")
    print("\n  Check Usage & Quotas:")
    print("     Google AI Studio: https://aistudio.google.com/app/apikey")
    print(
        "     Cloud Console Quotas: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas"
    )
    print("\n   Tips:")
    print("    - Monitor your usage to avoid hitting rate limits")
    print("    - Consider upgrading to paid tier for higher limits")
    print("    - Implement exponential backoff for rate limit errors")


if __name__ == "__main__":
    main()
