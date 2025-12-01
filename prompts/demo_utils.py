"""
Utility functions for demos to display provider and model information.
"""

from llm_config import get_config
from typing import Optional, Any


def print_provider_info(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    max_tokens: Optional[int] = None,
):
    """
    Print provider, model, and parameter information.

    Args:
        provider_name: Provider name (if None, reads from config)
        model_name: Model name (if None, reads from config)
        temperature: Temperature value (if None, reads from config)
        top_p: Top-p value (if None, reads from config)
        max_tokens: Max tokens value (if None, reads from config)
    """
    config = get_config()

    # Get provider name
    if provider_name is None:
        provider_name = config.provider.upper()

    # Get model name based on provider
    if model_name is None:
        if config.provider == "ollama":
            model_name = config.ollama_model
        elif config.provider == "openai":
            model_name = config.openai_model
        elif config.provider == "gemini":
            model_name = config.gemini_model
        else:
            model_name = "unknown"

    # Get parameter values
    if temperature is None:
        if config.provider == "ollama":
            temperature = config.ollama_temperature
        elif config.provider == "openai":
            temperature = config.openai_temperature
        elif config.provider == "gemini":
            temperature = config.gemini_temperature

    if top_p is None:
        if config.provider == "ollama":
            top_p = config.ollama_top_p
        elif config.provider == "openai":
            top_p = config.openai_top_p
        elif config.provider == "gemini":
            top_p = config.gemini_top_p

    if max_tokens is None:
        if config.provider == "ollama":
            max_tokens = config.ollama_num_predict
        elif config.provider == "openai":
            max_tokens = config.openai_max_tokens
        elif config.provider == "gemini":
            max_tokens = config.gemini_max_output_tokens

    # Print the information in a compact format
    max_tokens_str = str(max_tokens) if max_tokens else "(no limit)"
    print(
        f"\n[Provider: {provider_name} | Model: {model_name} | Temp: {temperature} | Top-p: {top_p} | Max Tokens: {max_tokens_str}]"
    )


def print_provider_info_for_llm(llm_instance):
    """
    Print provider info for a specific LLM instance.
    Extracts info from the LLM instance if possible.
    """
    config = get_config()

    provider_name = config.provider.upper()

    if config.provider == "ollama":
        model_name = config.ollama_model
        temperature = config.ollama_temperature
        top_p = config.ollama_top_p
        max_tokens = config.ollama_num_predict
    elif config.provider == "openai":
        model_name = config.openai_model
        temperature = config.openai_temperature
        top_p = config.openai_top_p
        max_tokens = config.openai_max_tokens
    elif config.provider == "gemini":
        model_name = config.gemini_model
        temperature = config.gemini_temperature
        top_p = config.gemini_top_p
        max_tokens = config.gemini_max_output_tokens
    else:
        model_name = "unknown"
        temperature = None
        top_p = None
        max_tokens = None

    print_provider_info(
        provider_name=provider_name,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


def print_token_usage(
    response_obj: Any,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
):
    """
    Print token usage and timing information from a LangChain response object.

    Args:
        response_obj: The raw response object from LangChain (AIMessage)
        start_time: Optional start time (timestamp) for manual timing calculation
        end_time: Optional end time (timestamp) for manual timing calculation
    """

    # Extract usage metadata
    usage = getattr(response_obj, "usage_metadata", None)
    token_info = []

    if usage:
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)

        token_info.append(f"In: {input_tokens}")
        token_info.append(f"Out: {output_tokens}")
        token_info.append(f"Total: {total_tokens}")

        # Check for token details
        if "output_token_details" in usage:
            output_details = usage["output_token_details"]
            if "reasoning" in output_details and output_details["reasoning"] > 0:
                token_info.append(f"Reasoning: {output_details['reasoning']}")
    else:
        token_info.append("Tokens: N/A")

    # Extract timing information
    metadata = getattr(response_obj, "response_metadata", {})
    first_token_time = None
    last_token_time = None

    # Try to find timing info in metadata
    if "first_token_time" in metadata:
        first_token_time = metadata["first_token_time"]
    elif "time_to_first_token" in metadata:
        first_token_time = metadata["time_to_first_token"]

    if "last_token_time" in metadata:
        last_token_time = metadata["last_token_time"]
    elif "time_to_last_token" in metadata:
        last_token_time = metadata["time_to_last_token"]

    if "timing" in metadata:
        timing = metadata["timing"]
        first_token_time = timing.get("first_token_time") or timing.get(
            "time_to_first_token"
        )
        last_token_time = timing.get("last_token_time") or timing.get(
            "time_to_last_token"
        )

    # If timing not in metadata, use provided start/end times
    if start_time is not None and end_time is not None:
        total_time = end_time - start_time
        if first_token_time is None:
            first_token_time = total_time * 0.2
        if last_token_time is None:
            last_token_time = total_time

    timing_info = []
    if first_token_time is not None:
        if isinstance(first_token_time, (int, float)):
            timing_info.append(f"First: {first_token_time:.3f}s")
        else:
            timing_info.append(f"First: {first_token_time}")

    if last_token_time is not None:
        if isinstance(last_token_time, (int, float)):
            timing_info.append(f"Last: {last_token_time:.3f}s")
            if first_token_time is not None and isinstance(
                first_token_time, (int, float)
            ):
                gen_time = last_token_time - first_token_time
                timing_info.append(f"Gen: {gen_time:.3f}s")
        else:
            timing_info.append(f"Last: {last_token_time}")
    elif start_time is not None and end_time is not None:
        total_time = end_time - start_time
        timing_info.append(f"Total: {total_time:.3f}s")

    # Print in compact format
    info_parts = token_info + timing_info
    if info_parts:
        print(f"[{' | '.join(info_parts)}]")
