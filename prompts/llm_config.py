"""
Configuration system for LLM providers.
Allows easy switching between providers via configuration.
"""

import os
from typing import Optional, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from llm_providers import LLMProvider, OllamaProvider, OpenAIProvider
from llm_providers import GeminiProvider

# Load environment variables from .env file
# Try both .env and .venv files
load_dotenv(".env")


class OllamaConfig(BaseModel):
    """Configuration for Ollama provider."""

    model: str = "deepseek-r1-32b:latest"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    top_p: float = 0.9
    num_predict: Optional[int] = None


class OpenAIConfig(BaseModel):
    """Configuration for OpenAI provider."""

    model: str = "gpt-3.5-turbo"  # More widely available model
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    top_p: float = 1.0
    max_tokens: Optional[int] = None


class GeminiConfig(BaseModel):
    """Configuration for Gemini provider."""

    model: str = "gemini-pro"
    api_key: Optional[str] = None
    temperature: float = 0.7
    top_p: float = 0.95
    max_output_tokens: Optional[int] = None


class LLMConfig(BaseSettings):
    """Main LLM configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Provider selection
    provider: Literal["ollama", "openai", "gemini"] = Field(
        default="ollama", description="LLM provider to use"
    )

    # Ollama configuration
    ollama_model: str = Field(default="deepseek-r1-32b:latest")
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_temperature: float = Field(default=0.7)
    ollama_top_p: float = Field(default=0.9)
    ollama_num_predict: Optional[int] = Field(default=None)

    # OpenAI configuration
    openai_model: str = Field(default="gpt-3.5-turbo")  # More widely available
    openai_api_key: Optional[str] = Field(default=None)
    openai_base_url: Optional[str] = Field(default=None)
    openai_temperature: float = Field(default=0.7)
    openai_top_p: float = Field(default=1.0)
    openai_max_tokens: Optional[int] = Field(default=None)

    # Gemini configuration
    gemini_model: str = Field(default="gemini-2.5-flash")
    gemini_api_key: Optional[str] = Field(default=None)
    gemini_temperature: float = Field(default=0.7)
    gemini_top_p: float = Field(default=0.95)
    gemini_max_output_tokens: Optional[int] = Field(default=None)

    def get_ollama_config(self) -> OllamaConfig:
        """Get Ollama configuration."""
        return OllamaConfig(
            model=self.ollama_model,
            base_url=self.ollama_base_url,
            temperature=self.ollama_temperature,
            top_p=self.ollama_top_p,
            num_predict=self.ollama_num_predict,
        )

    def get_openai_config(self) -> OpenAIConfig:
        """Get OpenAI configuration."""
        # Try to get API key from config, then env var
        # load_dotenv() was called at module level, so os.getenv should work
        api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")

        # If still None, ChatOpenAI will try to get it from env itself
        # but we'll let it handle the error if it's truly missing

        return OpenAIConfig(
            model=self.openai_model,
            api_key=api_key,
            base_url=self.openai_base_url,
            temperature=self.openai_temperature,
            top_p=self.openai_top_p,
            max_tokens=self.openai_max_tokens,
        )

    def get_gemini_config(self) -> GeminiConfig:
        """Get Gemini configuration."""
        # Try to get API key from config, then env var
        # load_dotenv() was called at module level, so os.getenv should work
        api_key = self.gemini_api_key or os.getenv("GOOGLE_API_KEY")

        # If still None, ChatGoogleGenerativeAI will try to get it from env itself
        # but we'll let it handle the error if it's truly missing

        return GeminiConfig(
            model=self.gemini_model,
            api_key=api_key,
            temperature=self.gemini_temperature,
            top_p=self.gemini_top_p,
            max_output_tokens=self.gemini_max_output_tokens,
        )

    def create_provider(self) -> LLMProvider:
        """
        Create an LLM provider based on the current configuration.

        Returns:
            LLMProvider instance
        """
        if self.provider == "ollama":
            config = self.get_ollama_config()
            return OllamaProvider(
                model=config.model,
                base_url=config.base_url,
                temperature=config.temperature,
                top_p=config.top_p,
                num_predict=config.num_predict,
            )

        elif self.provider == "openai":
            config = self.get_openai_config()
            return OpenAIProvider(
                model=config.model,
                api_key=config.api_key,
                base_url=config.base_url,
                temperature=config.temperature,
                top_p=config.top_p,
                max_tokens=config.max_tokens,
            )

        elif self.provider == "gemini":
            config = self.get_gemini_config()
            return GeminiProvider(
                model=config.model,
                api_key=config.api_key,
                temperature=config.temperature,
                top_p=config.top_p,
                max_output_tokens=config.max_output_tokens,
            )

        else:
            raise ValueError(f"Unknown provider: {self.provider}")


# Global configuration instance
_config: Optional[LLMConfig] = None


def get_config() -> LLMConfig:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = LLMConfig()
    return _config


def get_llm() -> LLMProvider:
    """
    Get an LLM provider instance based on the current configuration.

    Returns:
        LLMProvider instance
    """
    config = get_config()
    return config.create_provider()
