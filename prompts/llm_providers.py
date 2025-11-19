"""
LLM provider implementations for Ollama, OpenAI, and Gemini.
"""

from typing import Iterator, List, Union, Optional
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from llm_interface import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation."""
    
    def __init__(
        self,
        model: str = "deepseek-r1-32b:latest",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_predict: Optional[int] = None,
    ):
        """
        Initialize Ollama provider.
        
        Args:
            model: Model name (e.g., "deepseek-r1-32b:latest")
            base_url: Ollama API base URL
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            num_predict: Maximum tokens to generate
        """
        self.model_name = model
        self.base_url = base_url
        self.temperature = temperature
        self.top_p = top_p
        self.num_predict = num_predict
        
        self._llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
            top_p=top_p,
            num_predict=num_predict,
        )
    
    def invoke(self, prompt: Union[str, List[BaseMessage]]) -> str:
        """Invoke the LLM with a prompt."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        response = self._llm.invoke(prompt)
        return response.content
    
    def invoke_with_metadata(self, prompt: Union[str, List[BaseMessage]]):
        """
        Invoke the LLM and return both content, raw response object, and timing.
        
        Returns:
            tuple: (content: str, response_object: Any, start_time: float, end_time: float)
        """
        import time
        
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        start_time = time.time()
        response = self._llm.invoke(prompt)
        end_time = time.time()
        
        return response.content, response, start_time, end_time
    
    def stream(self, prompt: Union[str, List[BaseMessage]]) -> Iterator[str]:
        """Stream responses from the LLM."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        for chunk in self._llm.stream(prompt):
            if chunk.content:
                yield chunk.content
    
    def batch(self, prompts: List[str]) -> List[str]:
        """Process multiple prompts in batch."""
        messages_list = [[HumanMessage(content=p)] for p in prompts]
        responses = self._llm.batch(messages_list)
        return [r.content for r in responses]
    
    def get_model(self) -> BaseChatModel:
        """Get the underlying LangChain model instance."""
        return self._llm
    
    def update_parameters(
        self,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
    ) -> "OllamaProvider":
        """Update model parameters and return a new instance."""
        return OllamaProvider(
            model=self.model_name,
            base_url=self.base_url,
            temperature=temperature if temperature is not None else self.temperature,
            top_p=top_p if top_p is not None else self.top_p,
            num_predict=max_tokens if max_tokens is not None else self.num_predict,
        )


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            model: Model name (e.g., "gpt-3.5-turbo", "gpt-4", "gpt-4o-mini")
            api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
            base_url: Custom base URL (for OpenAI-compatible APIs)
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        
        kwargs = {
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
        }
        
        # Always pass api_key if provided, otherwise let ChatOpenAI use env var
        if api_key is not None:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["base_url"] = base_url
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        self._llm = ChatOpenAI(**kwargs)
    
    def invoke(self, prompt: Union[str, List[BaseMessage]]) -> str:
        """Invoke the LLM with a prompt."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        response = self._llm.invoke(prompt)
        return response.content
    
    def invoke_with_metadata(self, prompt: Union[str, List[BaseMessage]]):
        """
        Invoke the LLM and return both content, raw response object, and timing.
        
        Returns:
            tuple: (content: str, response_object: Any, start_time: float, end_time: float)
        """
        import time
        
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        start_time = time.time()
        response = self._llm.invoke(prompt)
        end_time = time.time()
        
        return response.content, response, start_time, end_time
    
    def stream(self, prompt: Union[str, List[BaseMessage]]) -> Iterator[str]:
        """Stream responses from the LLM."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        for chunk in self._llm.stream(prompt):
            if chunk.content:
                yield chunk.content
    
    def batch(self, prompts: List[str]) -> List[str]:
        """Process multiple prompts in batch."""
        messages_list = [[HumanMessage(content=p)] for p in prompts]
        responses = self._llm.batch(messages_list)
        return [r.content for r in responses]
    
    def get_model(self) -> BaseChatModel:
        """Get the underlying LangChain model instance."""
        return self._llm
    
    def update_parameters(
        self,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
    ) -> "OpenAIProvider":
        """Update model parameters and return a new instance."""
        return OpenAIProvider(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature if temperature is not None else self.temperature,
            top_p=top_p if top_p is not None else self.top_p,
            max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
        )


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider implementation."""
    
    def __init__(
        self,
        model: str = "gemini-pro",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.95,
        max_output_tokens: Optional[int] = None,
    ):
        """
        Initialize Gemini provider.
        
        Args:
            model: Model name (e.g., "gemini-pro", "gemini-1.5-pro")
            api_key: Google API key (if None, uses GOOGLE_API_KEY env var)
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            max_output_tokens: Maximum tokens to generate
        """
        self.model_name = model
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        self.max_output_tokens = max_output_tokens
        
        kwargs = {
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
        }
        
        if api_key:
            kwargs["google_api_key"] = api_key
        if max_output_tokens:
            kwargs["max_output_tokens"] = max_output_tokens
        
        self._llm = ChatGoogleGenerativeAI(**kwargs)
    
    def invoke(self, prompt: Union[str, List[BaseMessage]]) -> str:
        """Invoke the LLM with a prompt."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        response = self._llm.invoke(prompt)
        return response.content
    
    def invoke_with_metadata(self, prompt: Union[str, List[BaseMessage]]):
        """
        Invoke the LLM and return both content, raw response object, and timing.
        
        Returns:
            tuple: (content: str, response_object: Any, start_time: float, end_time: float)
        """
        import time
        
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        start_time = time.time()
        response = self._llm.invoke(prompt)
        end_time = time.time()
        
        return response.content, response, start_time, end_time
    
    def stream(self, prompt: Union[str, List[BaseMessage]]) -> Iterator[str]:
        """Stream responses from the LLM."""
        if isinstance(prompt, str):
            prompt = [HumanMessage(content=prompt)]
        
        for chunk in self._llm.stream(prompt):
            if chunk.content:
                yield chunk.content
    
    def batch(self, prompts: List[str]) -> List[str]:
        """Process multiple prompts in batch."""
        messages_list = [[HumanMessage(content=p)] for p in prompts]
        responses = self._llm.batch(messages_list)
        return [r.content for r in responses]
    
    def get_model(self) -> BaseChatModel:
        """Get the underlying LangChain model instance."""
        return self._llm
    
    def update_parameters(
        self,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
    ) -> "GeminiProvider":
        """Update model parameters and return a new instance."""
        return GeminiProvider(
            model=self.model_name,
            api_key=self.api_key,
            temperature=temperature if temperature is not None else self.temperature,
            top_p=top_p if top_p is not None else self.top_p,
            max_output_tokens=max_tokens if max_tokens is not None else self.max_output_tokens,
        )

