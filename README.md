# Prompt Engineering & LangChain Demos

A comprehensive demonstration framework covering:
- **Prompt Engineering**: Advanced prompting techniques and parameter tuning
- **LangChain**: Complete LangChain 1.0 examples with LCEL, RAG, Agents, and more

Supports multiple LLM providers (Ollama, OpenAI, Gemini) via a unified interface.

## Features

- **Abstract LLM Interface**: Switch between providers seamlessly
- **Multiple Providers**: Support for Ollama, OpenAI, and Google Gemini
- **Modular Demos**: Each prompt technique in a separate file
- **Easy Configuration**: Simple config file or environment variables
- **Comprehensive Prompting Techniques**: Covers all major prompting strategies from 2025 best practices
- **Token Usage & Timing**: All demos display token usage and timing information
- **Student-Friendly**: Designed for teaching LLM behavior, parameter tuning, and prompt engineering

## Installation

```bash
# Install dependencies
uv sync
```

## Configuration

### Option 1: Environment Variables (Recommended)

Create a `.env` file from the example:

```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API keys and model preferences
```

**Example `.env` file:**

```bash
# Set your provider
PROVIDER=openai  # or "ollama" or "gemini"

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo  # Options: gpt-3.5-turbo, gpt-4, gpt-4o-mini, gpt-4-turbo

# Ollama Configuration (if using Ollama)
OLLAMA_MODEL=deepseek-r1-32b:latest
OLLAMA_BASE_URL=http://localhost:11434

# Gemini Configuration (if using Gemini)
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-pro
```

**Important:** Both `PROVIDER` and model names (e.g., `OPENAI_MODEL`, `GEMINI_MODEL`, `OLLAMA_MODEL`) are automatically read from your `.env` file. All demos will use the provider and model specified in your `.env` file.

### Option 2: Python Configuration (Override .env)

You can also override `.env` settings programmatically:

```python
from llm_config import LLMConfig, get_llm

# Create custom config (overrides .env)
from llm_config import get_config
base_config = get_config()  # Get current .env config

config = LLMConfig(
    provider="openai",
    openai_model=base_config.openai_model,  # Use model from .env
    openai_api_key="your-key"  # Override API key from .env
)

# Get LLM instance
llm = config.create_provider()
```

**Note:** Settings in `.env` file are loaded automatically. Python config overrides them if specified.

## Usage

### Run Individual Demos

#### Teaching Order (Recommended Sequence)

```bash
# 1. Start with basic invocation
python 1_demo_basic_invoke.py

# 2. Understand parameter tuning (temperature, top_p, max_tokens)
python 2_demo_parameter_tuning.py

# 3. Advanced parameter combinations
python 3_demo_advanced_parameters.py

# 4. Basic prompt techniques (zero-shot, few-shot, chain-of-thought, role-based)
python 4_demo_prompt_techniques.py

# 5. Prompt iteration and refinement
python 5_demo_prompt_iteration.py

# 6. Structured prompts with LangChain templates
python 6_demo_structured_prompts.py

# 7. Model-specific templates (Markdown for ChatGPT/Gemini, XML for Claude)
python 7_demo_model_specific_templates.py

# 8. Universal cross-model compatible template
python 8_demo_universal_template.py

# 9. Format-constrained outputs (tables, code blocks, JSON, structured lists)
python 9_demo_format_constrained.py

# 10. Context-grounded prompts (rich context for better responses)
python 10_demo_context_grounded.py

# 11. Structured section prompts (Markdown sections, XML structure)
python 11_demo_structured_sections.py

# 12. Streaming responses (real-time token streaming)
python 12_demo_streaming.py
```

### Run All Demos

```bash
# Run all prompt engineering demos
python run_all_demos.py

# Run all LangChain examples (in teaching order)
for file in [0-9]_langchain_*.py; do
    echo "Running $file..."
    uv run python "$file"
    echo ""
done
```

### LangChain Examples (Separate Series)

A complete set of LangChain examples based on the 2025 AI Engineering curriculum:

```bash
# 1. Hello LangChain 1.0 (LCEL basics)
uv run python 1_langchain_hello_lcel.py

# 2. Core Prompt Engineering Techniques
uv run python 2_langchain_prompt_engineering.py

# 3. Self-Reflection Pattern
uv run python 3_langchain_self_reflection.py

# 4. Advanced LCEL Patterns (branching, streaming, retries)
uv run python 4_langchain_runnables_lcel.py

# 5. Basic RAG Pipeline
uv run python 5_langchain_rag_basic.py

# 6. Memory Systems
uv run python 6_langchain_memory.py

# 7. Agents and Tool Calling
uv run python 7_langchain_agents_tools.py

# 8. LangGraph Concepts (stateful, cyclic applications)
uv run python 8_langchain_langgraph.py
```

See `LANGCHAIN_EXAMPLES_README.md` for detailed documentation of each LangChain example.

## Using the LLM Interface in Your Code

```python
from llm_config import get_llm

# Get configured LLM provider
llm = get_llm()

# Simple invoke
response = llm.invoke("Explain quantum computing")

# Streaming
for chunk in llm.stream("Tell me a story"):
    print(chunk, end="")

# Batch processing
responses = llm.batch([
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?"
])

# Update parameters
creative_llm = llm.update_parameters(
    temperature=1.2,
    top_p=0.95,
    max_tokens=500
)
response = creative_llm.invoke("Write a poem")
```

## Provider Setup

### Ollama

1. Install Ollama: https://ollama.ai
2. Pull the model:
   ```bash
   ollama pull deepseek-r1-32b:latest
   ```
3. Start Ollama server:
   ```bash
   ollama serve
   ```

### OpenAI

1. Get API key from https://platform.openai.com
2. Set in `.env`:
   ```bash
   PROVIDER=openai
   OPENAI_API_KEY=sk-...
   ```

### Gemini

1. Get API key from https://makersuite.google.com/app/apikey
2. Set in `.env`:
   ```bash
   PROVIDER=gemini
   GOOGLE_API_KEY=...
   ```

## Project Structure

```
.
├── llm_interface.py          # Abstract base class
├── llm_providers.py          # Provider implementations
├── llm_config.py             # Configuration system
├── demo_utils.py             # Utility functions for demos
├── 1_demo_basic_invoke.py      # Basic LLM invoke
├── 2_demo_parameter_tuning.py  # Parameter tuning examples
├── 3_demo_advanced_parameters.py # Advanced parameter combinations
├── 4_demo_prompt_techniques.py # Basic prompt techniques (zero-shot, few-shot, CoT, role-based)
├── 5_demo_prompt_iteration.py  # Prompt refinement and iteration
├── 6_demo_structured_prompts.py # LangChain templates
├── 7_demo_model_specific_templates.py # Model-specific templates (Markdown/XML)
├── 8_demo_universal_template.py # Universal cross-model template
├── 9_demo_format_constrained.py # Format-constrained outputs (tables, code, JSON)
├── 10_demo_context_grounded.py  # Context-grounded prompts
├── 11_demo_structured_sections.py # Structured section prompts
├── 12_demo_streaming.py         # Streaming responses
├── run_all_demos.py          # Run all prompt engineering demos
│
├── 1_langchain_hello_lcel.py      # Hello LangChain 1.0 (LCEL)
├── 2_langchain_prompt_engineering.py # Core prompt engineering
├── 3_langchain_self_reflection.py  # Self-reflection pattern
├── 4_langchain_runnables_lcel.py   # Advanced LCEL patterns
├── 5_langchain_rag_basic.py        # Basic RAG pipeline
├── 6_langchain_memory.py           # Memory systems
├── 7_langchain_agents_tools.py     # Agents and tool calling
├── 8_langchain_langgraph.py        # LangGraph concepts
└── LANGCHAIN_EXAMPLES_README.md    # LangChain examples documentation
```

## Switching Providers

### Method 1: Update `.env` file (Easiest)

Simply edit your `.env` file and change the `PROVIDER`:

```bash
# Switch to OpenAI
PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Switch to Gemini
PROVIDER=gemini
GOOGLE_API_KEY=...
GEMINI_MODEL=gemini-pro

# Switch to Ollama
PROVIDER=ollama
OLLAMA_MODEL=deepseek-r1-32b:latest
```

### Method 2: Python Code

```python
from llm_config import LLMConfig

# Switch to OpenAI
config = LLMConfig(provider="openai", openai_api_key="...")
llm = config.create_provider()

# Switch to Gemini
config = LLMConfig(provider="gemini", gemini_api_key="...")
llm = config.create_provider()

# Switch to Ollama
config = LLMConfig(provider="ollama")
llm = config.create_provider()
```

**All demos automatically use the provider and model from your `.env` file!**

