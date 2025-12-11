# LangChain & Prompt Engineering Demonstrations

A comprehensive collection of examples demonstrating LangChain 1.0+ patterns, prompt engineering techniques, and AI application development with multiple LLM providers.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [LangChain Examples](#langchain-examples)
- [Prompt Engineering Examples](#prompt-engineering-examples)
- [Testing Tools](#testing-tools)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

## Overview

This repository contains production-ready examples of:

- **LangChain 1.0+ Patterns**: LCEL, Runnables, Agents, Memory, RAG
- **LangGraph Workflows**: Stateful multi-agent applications
- **Prompt Engineering**: Techniques for optimal LLM responses
- **Multi-Provider Support**: Ollama, OpenAI, Google Gemini
- **Advanced Techniques**: Chain-of-Thought, Tree-of-Thought, Self-Reflection

### Key Features

- LangChain 1.0+ compatible (uses modern Runnable interface)
- Type-safe with proper annotations
- PEP 8 compliant code
- Comprehensive inline documentation
- Real-world use cases and examples
- No deprecated patterns

## Setup

### Prerequisites

- Python 3.11+
- UV package manager (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd prompt-demo
```

2. Install dependencies using UV:
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

3. Configure environment variables:
```bash
cp env.example .env
# Edit .env and add your API keys
```

### API Keys

Add your API keys to `.env`:

```bash
# Google Gemini (recommended for examples)
GOOGLE_API_KEY=your-google-api-key-here

# Optional: Other providers
OPENAI_API_KEY=your-openai-api-key-here
OLLAMA_BASE_URL=http://localhost:11434
```

Get API keys:
- Google Gemini: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

## LangChain Examples

### Core Examples (Numbered 0-10)

#### 0. Sample LangChain (`0_sample_langchain.py`)
Basic LangChain introduction and setup.

#### 1. Hello LCEL (`1_langchain_hello_lcel.py`)
Introduction to LangChain Expression Language (LCEL).
- Basic chain creation with | operator
- Simple prompt templates
- Output parsing

#### 2. Prompt Engineering (`2_langchain_prompt_engineering.py`)
Prompt engineering techniques with LangChain.
- Template design
- Few-shot learning
- System messages

#### 3. Self-Reflection (`3_langchain_self_reflection.py`)
Self-reflection patterns for improved responses.
- Draft → Critique → Revise pattern
- Uses RunnablePassthrough.assign() (modern LCEL pattern)
- Iterative improvement through self-critique

#### 4. Chain-of-Thought, Tree-of-Thought (`4_cot_tot_got.py`)
Advanced reasoning techniques.
- Chain-of-Thought (CoT): Step-by-step reasoning
- Tree-of-Thought (ToT): Multiple reasoning paths
- Graph-of-Thought (GoT): Connected reasoning

#### 5. LangChain ToT/GoT (`5_langchain_tot_got.py`)
LangChain implementation of advanced reasoning.
- Structured reasoning with LangChain
- Multi-path exploration

#### 6. Runnables & LCEL (`6_langchain_runnables_lcel.py`)
Deep dive into the Runnable interface.
- Chain composition
- Parallel execution
- Custom runnables

#### 7. RAG - Retrieval-Augmented Generation (`7_langchain_rag_basic.py`)
Complete RAG pipeline implementation with in-memory vector store.

**What is RAG?**
- Retrieval: Find relevant information from knowledge base
- Augmentation: Add retrieved context to the query
- Generation: LLM generates answer based on context

**Benefits:**
- Reduces hallucinations
- Enables access to current/domain-specific data
- More cost-effective than fine-tuning

**Example Use Case:**
Uses an unpublished movie screenplay ("The Last Cipher" by Director Sofia Ramirez) to demonstrate how RAG allows the LLM to answer questions about content it was never trained on.

**Components:**
- Custom SimpleVectorStore for demonstration
- Embedding model (Gemini embedding-001)
- LCEL chain for retrieval + generation
- Cosine similarity for semantic search

#### 7.1. RAG with ChromaDB (`7_1_langchain_rag_chromadb.py`)
Production-ready RAG using ChromaDB vector database.

**ChromaDB Features:**
- Persistent storage (saves to disk)
- Fast similarity search with optimized indexing
- Metadata filtering capabilities
- Multiple distance metrics (L2, cosine, inner product)
- Production-ready and scalable

**Advanced Features Demonstrated:**
- Similarity search with relevance scores
- Metadata filtering (filter by author, year, etc.)
- MMR (Maximal Marginal Relevance) for diverse results
- Persistent storage in `./chroma_db` directory

**Installation Required:**
```bash
pip install chromadb langchain-chroma
```

**When to Use ChromaDB vs In-Memory:**
- Use ChromaDB for production applications
- Use in-memory store for quick prototypes/demos
- ChromaDB handles larger datasets efficiently
- Persistent storage survives application restarts

#### 8. Memory Systems (`8_langchain_memory.py`)
Conversation memory patterns (LangChain 1.0+).

**Memory Strategies:**
1. **Simple In-Memory History**: Stores all messages
   - Use case: Short conversations, customer support
   
2. **Windowed Memory**: Keeps only last N messages
   - Use case: Long conversations, token limit management

**Key Pattern:**
```python
RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)
```

**Deprecated Patterns (Don't Use):**
- ConversationBufferMemory
- ConversationSummaryMemory
- All langchain.memory.* classes

#### 9. Agents & Tools (`9_langchain_agents_tools.py`)
Modern agent patterns with tool calling.

**What are Agents?**
Agents use LLMs to:
1. Reason about which tools to use
2. Act by calling tools
3. Observe the results
4. Repeat until task complete

**Tools Demonstrated:**
- Calculator: Mathematical expressions
- Knowledge base search: Information retrieval
- Weather API: Simulated external data

**Pattern:**
- Uses @tool decorator (LangChain 1.0+ standard)
- .bind_tools() for tool binding
- Native LLM tool calling (Gemini, GPT-4, Claude)

#### 10. LangGraph - Stateful Workflows (`10_langchain_langgraph.py`)
Advanced graph-based orchestration.

**What is LangGraph?**
Library for building stateful, multi-actor applications with LLMs.

**Examples:**
1. **Simple Chatbot with Memory**
   - Uses StateGraph and MemorySaver
   - Persistent conversation state
   
2. **Research Agent with Tools**
   - Conditional routing
   - Tool execution with ToolNode
   
3. **Content Creation Workflow**
   - Multi-step pipeline: Outline -> Draft -> Review -> Finalize
   - Complex state management

**When to Use:**
- Multi-step workflows with state
- Cyclic processes (loops, retries)
- Human-in-the-loop workflows
- Multi-agent collaboration

## Prompt Engineering Examples

Located in `prompts/` directory:

### Prompt Techniques (`prompts/`)

1. **Basic Invoke** (`1_demo_basic_invoke.py`)
   - Simple LLM invocation
   - Basic prompt patterns

2. **Parameter Tuning** (`2_demo_parameter_tuning.py`)
   - Temperature, top_p, max_tokens
   - Impact on output quality

3. **Advanced Parameters** (`3_demo_advanced_parameters.py`)
   - Frequency penalty, presence penalty
   - Top-k sampling

4. **Prompt Techniques** (`4_demo_prompt_techniques.py`)
   - Few-shot learning
   - Chain-of-Thought
   - Role prompting

5. **Prompt Iteration** (`5_demo_prompt_iteration.py`)
   - Iterative refinement
   - A/B testing prompts

6. **Structured Prompts** (`6_demo_structured_prompts.py`)
   - JSON output
   - Pydantic models

7. **Model-Specific Templates** (`7_demo_model_specific_templates.py`)
   - Optimized prompts per model
   - Provider-specific patterns

8. **Universal Template** (`8_demo_universal_template.py`)
   - Cross-model compatibility
   - Provider-agnostic patterns

9. **Format-Constrained** (`9_demo_format_constrained.py`)
   - Output formatting
   - Structured responses

10. **Context-Grounded** (`10_demo_context_grounded.py`)
    - Grounding responses in context
    - Reducing hallucinations

11. **Structured Sections** (`11_demo_structured_sections.py`)
    - Multi-section outputs
    - Complex formatting

12. **Streaming** (`12_demo_streaming.py`)
    - Real-time response streaming
    - Token-by-token output

### Supporting Modules

- **llm_config.py**: Multi-provider configuration system
- **llm_providers.py**: Provider implementations (Ollama, OpenAI, Gemini)
- **llm_interface.py**: Unified interface for all providers
- **demo_utils.py**: Utility functions for demos

## Testing Tools

### Test Gemini API Key

#### `test_gemini_key.py` - Pure Python (No Dependencies)
Tests Gemini API key using only Python standard library.

**Features:**
- API key validation
- Lists all available models (9 total: 7 generative, 2 embedding)
- Shows exact token usage per request
- Quota monitoring information
- No external dependencies (uses urllib)

**Run:**
```bash
python3 test_gemini_key.py
```

#### `test_gemini_langchain.py` - LangChain Integration
Tests Gemini API with LangChain patterns.

**Features:**
- API key validation with LangChain
- Tests multiple models
- Streaming demonstration
- Token counting capabilities
- Production-ready patterns

**Run:**
```bash
uv run test_gemini_langchain.py
```

### Available Gemini Models

**Generative Models:**
- gemini-2.5-flash: 1M input / 65K output tokens (recommended)
- gemini-2.5-pro: 1M input / 65K output tokens (most capable)
- gemini-2.0-flash: 1M input / 8K output tokens
- gemini-2.0-flash-lite: 1M input / 8K output tokens
- gemini-2.5-flash-lite: 1M input / 65K output tokens

**Embedding Models:**
- text-embedding-004
- embedding-001

### Quota Information

**Free Tier Limits:**
- 15 requests per minute (RPM)
- 1,000,000 tokens per minute (TPM)
- 1,500 requests per day (RPD)

**Monitor Usage:**
- Google AI Studio: https://aistudio.google.com/app/apikey
- Cloud Console: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas

## Project Structure

```
prompt-demo/
├── 0_sample_langchain.py          # Basic LangChain intro
├── 1_langchain_hello_lcel.py      # LCEL introduction
├── 2_langchain_prompt_engineering.py  # Prompt patterns
├── 3_langchain_self_reflection.py # Self-reflection with RunnablePassthrough
├── 4_cot_tot_got.py               # Advanced reasoning
├── 5_langchain_tot_got.py         # LangChain reasoning
├── 6_langchain_runnables_lcel.py  # Runnables deep dive
├── 7_langchain_rag_basic.py       # RAG with in-memory vector store
├── 7_1_langchain_rag_chromadb.py  # RAG with ChromaDB (production)
├── 8_langchain_memory.py          # Memory systems
├── 9_langchain_agents_tools.py    # Agents & tools
├── 10_langchain_langgraph.py      # LangGraph workflows
├── 11_local_prompt_engineering.py # Local model prompting
├── prompts/                       # Prompt engineering demos
│   ├── 1_demo_basic_invoke.py
│   ├── 2_demo_parameter_tuning.py
│   ├── 3_demo_advanced_parameters.py
│   └── ... (12 total demos)
├── test_gemini_key.py            # API key tester (pure Python)
├── test_gemini_langchain.py      # API key tester (LangChain)
├── run_all_demos.py              # Run all examples
├── pyproject.toml                # UV/pip dependencies
├── requirements.txt              # Pip dependencies
└── .env                          # Your API keys (not committed)
```

## Configuration

### Environment Variables

The project supports multiple LLM providers. Configure in `.env`:

```bash
# Provider Selection
PROVIDER=gemini  # Options: ollama, openai, gemini

# Google Gemini
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL=gemini-2.5-flash

# OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama (optional, for local models)
OLLAMA_MODEL=deepseek-r1-32b:latest
OLLAMA_BASE_URL=http://localhost:11434
```

### Switching Providers

The project uses a unified configuration system:

```python
from prompts.llm_config import get_llm

# Automatically uses provider from .env
llm = get_llm()
```

## Running Examples

### Run Individual Examples

```bash
# Using UV (recommended)
uv run python 1_langchain_hello_lcel.py
uv run python 3_langchain_self_reflection.py
uv run python 7_langchain_rag_basic.py
uv run python 7_1_langchain_rag_chromadb.py  # Requires chromadb
uv run python 10_langchain_langgraph.py

# Or directly with Python (if dependencies installed)
python3 7_langchain_rag_basic.py
python3 7_1_langchain_rag_chromadb.py
```

### Run All Examples

```bash
uv run python run_all_demos.py
```

## Best Practices

### LangChain 1.0+ Patterns

**DO Use:**
- LCEL with | operator for chaining
- Runnable interface (.invoke(), .stream(), .batch())
- RunnablePassthrough for data flow
- RunnableMap for parallel execution
- RunnableLambda for custom functions
- RunnableWithMessageHistory for memory
- @tool decorator for tool definitions
- StateGraph for complex workflows

**DON'T Use (Deprecated):**
- LLMChain, SimpleSequentialChain
- ConversationBufferMemory and related classes
- Old agent patterns (ZeroShot, Conversational)
- .run() or .predict() methods

### Understanding Runnables

**Core Runnable Types:**

1. **RunnablePassthrough**: Pass data through while optionally adding fields
   ```python
   # Preserves input, adds computed fields
   chain = RunnablePassthrough.assign(draft=draft_chain)
   ```

2. **RunnableMap** / **RunnableParallel**: Execute branches in parallel
   ```python
   # Runs french and summary simultaneously
   map_chain = RunnableMap({
       "french": translate_chain,
       "summary": summary_chain
   })
   ```

3. **RunnableLambda**: Wrap custom Python functions
   ```python
   # Add custom logic to chains
   chain = prompt | model | RunnableLambda(custom_parser)
   ```

4. **RunnableBranch**: Conditional routing
   ```python
   # Route based on conditions
   branch = RunnableBranch(
       (condition1, chain1),
       (condition2, chain2),
       default_chain
   )
   ```

**When to Use:**
- **RunnablePassthrough**: Self-reflection, multi-step enrichment
- **RunnableMap**: Multi-output generation, speed optimization
- **RunnableLambda**: Custom parsing, API calls, data transformation
- **RunnableBranch**: Multi-intent routing, dynamic prompts

**Key Insight**: Only RunnableMap/RunnableParallel execute in parallel—everything else is sequential!

### Code Standards

- **Python**: PEP 8 compliant
- **Line Length**: 88 characters (Black formatter standard)
- **Type Hints**: Used throughout for clarity
- **Documentation**: Comprehensive inline comments
- **Error Handling**: Graceful failures with helpful messages
- **Imports**: All imports at top of file, before any executable code

**Linting Configuration:**

Create `.flake8` in project root:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,.venv,venv,build,dist,chroma_db
```

**Formatting Tips:**
- Use parentheses for implicit line continuation
- Break long chains across multiple lines
- Use `# noqa: E501` sparingly for unavoidable long lines
- Extract complex expressions to variables for readability

### Memory Management

- Use RunnableWithMessageHistory for conversation memory
- Implement windowing for long conversations
- Store session history per user/thread
- Consider token limits when designing memory strategy

### Tool Calling

- Write clear, detailed docstrings (LLM reads these)
- Use type hints for all tool arguments
- Return strings for easier LLM parsing
- Handle errors gracefully
- Implement retry logic for production

## LangChain 1.0+ Migration Guide

### Key Changes from Pre-1.0

| Old (< 1.0) | New (1.0+) |
|-------------|-----------|
| `chain.run()` | `chain.invoke()` |
| `LLMChain(...)` | LCEL with `\|` |
| `langchain.llms` | `langchain_core` + providers |
| `ConversationBufferMemory` | `RunnableWithMessageHistory` |
| Manual chaining | Automatic with Runnable |

### Example Migration

**Old:**
```python
from langchain.chains import LLMChain
from langchain.llms import OpenAI

chain = LLMChain(llm=OpenAI(), prompt=prompt)
result = chain.run(input="Hello")
```

**New:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

chain = prompt | ChatOpenAI() | StrOutputParser()
result = chain.invoke({"input": "Hello"})
```

## Advanced Techniques

### RAG (Retrieval-Augmented Generation)

See `7_langchain_rag_basic.py` for basic implementation and `7_1_langchain_rag_chromadb.py` for production-ready version.

**Three Stages:**
1. **Indexing**: Convert documents to embeddings, store in vector DB
2. **Retrieval**: Find relevant documents via semantic search
3. **Generation**: LLM answers using retrieved context

**Vector Store Options:**
- **In-Memory** (`7_langchain_rag_basic.py`): Quick prototypes, demos
- **ChromaDB** (`7_1_langchain_rag_chromadb.py`): Production apps, persistent storage
- **Others**: FAISS, Pinecone, Weaviate, Qdrant

**When to Use:**
- Domain-specific knowledge
- Up-to-date information
- Reducing hallucinations
- Source attribution

**ChromaDB Advantages:**
- Persistent storage across sessions
- Metadata filtering (filter by author, date, category)
- MMR search for result diversity
- Better performance at scale

### LangGraph Workflows

See `10_langchain_langgraph.py` for examples.

**Core Concepts:**
- **StateGraph**: Define nodes and edges
- **Nodes**: Functions that process state
- **Edges**: Transitions between nodes
- **Checkpointing**: Persist state with MemorySaver

**Use Cases:**
- Multi-step workflows
- Human-in-the-loop processes
- Multi-agent collaboration
- Complex state management

## Troubleshooting

### Import Errors

If you see "module not resolved" errors in VS Code/Cursor:

1. Set Python interpreter:
   - Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
   - Type "Python: Select Interpreter"
   - Choose `.venv/bin/python`

2. Reload window:
   - Press Cmd+Shift+P
   - Type "Developer: Reload Window"

### API Key Issues

**"API key not found":**
- Ensure `.env` file exists with `GOOGLE_API_KEY=...`
- Check the key is not wrapped in quotes

**"403 Forbidden" or "API key leaked":**
- Your key was exposed publicly
- Generate a new key at Google AI Studio

**"429 Quota exceeded":**
- You've hit rate limits
- Wait for quota reset or upgrade to paid tier

### Rate Limits

If you hit rate limits:
- Implement exponential backoff
- Cache responses when appropriate
- Use batch requests
- Monitor your usage regularly

## Resources

### Documentation

- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Google Gemini**: https://ai.google.dev/docs
- **Prompt Engineering**: See `Prompt Engineering Notes.md`

### Additional Files

- **AI Engineering Vocabulary.md**: Comprehensive AI/ML terminology
- **Prompt Engineering Notes.md**: Detailed prompting techniques
- **env.example**: Template for environment configuration

## Contributing

When adding new examples:

1. Follow the numbering convention
2. Use LangChain 1.0+ patterns only
3. Add comprehensive documentation
4. Include use case descriptions
5. Test with multiple providers when possible
6. Follow PEP 8 style guidelines
7. No emojis in code or comments

## License

See LICENSE file for details.

## Support

For issues or questions:
1. Check existing examples for similar patterns
2. Review documentation in markdown files
3. Test API keys using test scripts
4. Verify dependencies with `uv pip list`

---

**Version**: 0.1.0  
**Python**: 3.11+  
**LangChain**: 1.0+  
**LangGraph**: 1.0+  

Last Updated: December 2024

