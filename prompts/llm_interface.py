"""
Abstract interface for LLM providers.
Allows switching between different providers (Ollama, OpenAI, Gemini) seamlessly.
"""

from abc import ABC, abstractmethod
from typing import Iterator, List, Union
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def invoke(self, prompt: Union[str, List[BaseMessage]]) -> str:
        """
        Invoke the LLM with a prompt.

        Args:
            prompt: Either a string or a list of BaseMessage objects

        Returns:
            The response content as a string
        """
        pass

    @abstractmethod
    def stream(self, prompt: Union[str, List[BaseMessage]]) -> Iterator[str]:
        """
        Stream responses from the LLM.

        Args:
            prompt: Either a string or a list of BaseMessage objects

        Yields:
            Response chunks as strings
        """
        pass

    @abstractmethod
    def batch(self, prompts: List[str]) -> List[str]:
        """
        Process multiple prompts in batch.

        Args:
            prompts: List of prompt strings

        Returns:
            List of response strings
        """
        pass

    @abstractmethod
    def get_model(self) -> BaseChatModel:
        """
        Get the underlying LangChain model instance.

        Returns:
            BaseChatModel instance
        """
        pass

    def update_parameters(
        self,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
    ) -> "LLMProvider":
        """
        Update model parameters and return a new instance with updated parameters.

        Args:
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens to generate

        Returns:
            New LLMProvider instance with updated parameters
        """
        # Default implementation - subclasses should override
        return self
