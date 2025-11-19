# LangChain Examples - Teaching Series

A complete set of LangChain examples based on the 2025 AI Engineering curriculum, demonstrating both LangChain functionality and prompt engineering techniques.

## Overview

These examples follow a progressive teaching order, starting with basic LCEL concepts and advancing to complex agentic workflows. All examples use **Gemini API** and are designed to be self-contained and easy to understand.

## Examples

### 1. `1_langchain_hello_lcel.py` - Hello LangChain 1.0 (LCEL)
**Concepts:**
- Basic LCEL chain composition with pipe operator (`|`)
- Sync and async invocation
- Prompt → Model → Parser pattern

**Key Takeaways:**
- Everything is a Runnable
- The `|` operator builds composable, type-safe pipelines
- Automatic support for sync/async/streaming

### 2. `2_langchain_prompt_engineering.py` - Core Prompt Engineering
**Concepts:**
- Role prompting (System messages)
- Zero-shot vs Few-shot prompting
- Chain-of-Thought (CoT) reasoning
- Structural prompting (XML tags)

**Key Takeaways:**
- System prompts set the model's persona
- Few-shot examples dramatically improve accuracy
- CoT forces step-by-step reasoning
- XML tags guide structured output

### 3. `3_langchain_self_reflection.py` - Self-Reflection Pattern
**Concepts:**
- Draft → Critique → Revise loop
- Using LLM to improve its own output
- RunnableMap for parallel execution

**Key Takeaways:**
- Self-critique improves output quality
- RunnableMap enables complex data flows
- Iterative refinement patterns

### 4. `4_langchain_runnables_lcel.py` - Advanced LCEL Patterns
**Concepts:**
- Branching with RunnableMap
- Streaming responses
- Error handling with retries
- RunnableLambda for custom functions

**Key Takeaways:**
- RunnableMap fans out parallel chains
- Streaming improves perceived latency
- `.with_retry()` adds resilience
- RunnableLambda integrates custom logic

### 5. `5_langchain_rag_basic.py` - Basic RAG Pipeline
**Concepts:**
- Retrieval-Augmented Generation
- Vector stores (FAISS)
- Embeddings
- Context augmentation

**Key Takeaways:**
- RAG = Retrieve → Augment → Generate
- Vector stores enable semantic search
- Embeddings capture semantic meaning
- Context grounding prevents hallucinations

### 6. `6_langchain_memory.py` - Memory Systems
**Concepts:**
- Conversation memory
- RunnableWithMessageHistory
- Multi-user sessions
- Session management

**Key Takeaways:**
- Memory enables context across turns
- RunnableWithMessageHistory is LCEL-native
- Session IDs isolate user conversations
- Memory can be persisted to databases

### 7. `7_langchain_agents_tools.py` - Agents and Tool Calling
**Concepts:**
- ReAct pattern (Reason → Act → Observe)
- Tool definition with `@tool` decorator
- AgentExecutor
- Tool binding to models

**Key Takeaways:**
- Agents can use external tools
- Tool docstrings are critical for LLM understanding
- `bind_tools()` makes tools available to the model
- AgentExecutor manages the ReAct loop

### 8. `8_langchain_langgraph.py` - LangGraph Stateful Applications
**Concepts:**
- State management with TypedDict
- Graph-based orchestration
- Conditional routing
- Cyclic workflows

**Key Takeaways:**
- LangGraph for stateful, cyclic applications
- State is shared across nodes
- Conditional edges enable routing
- Graphs compile to executable Runnables

## Setup

1. **Install dependencies:**
```bash
uv sync
```

2. **Set up environment:**
Create a `.env` file with your Gemini API key:
```bash
GOOGLE_API_KEY=your-api-key-here
```

3. **Run examples:**
```bash
# Run individual examples
uv run python 1_langchain_hello_lcel.py
uv run python 2_langchain_prompt_engineering.py
# ... etc

# Or run all in sequence
for file in [0-9]_langchain_*.py; do
    echo "Running $file..."
    uv run python "$file"
    echo ""
done
```

## Teaching Order

The examples are numbered in the recommended teaching sequence:

1. **Foundation** (Examples 1-2): Basic LCEL and prompt engineering
2. **Advanced Patterns** (Examples 3-4): Self-reflection and advanced LCEL
3. **Applications** (Examples 5-6): RAG and memory systems
4. **Agentic Systems** (Examples 7-8): Agents and graph-based workflows

## Key Concepts Demonstrated

### Prompt Engineering Techniques
- ✅ Role-based prompting
- ✅ Zero-shot and Few-shot learning
- ✅ Chain-of-Thought reasoning
- ✅ Structural prompting (XML)
- ✅ Self-critique and refinement

### LangChain Patterns
- ✅ LCEL composition
- ✅ RunnableMap for branching
- ✅ Streaming responses
- ✅ Error handling and retries
- ✅ Memory management
- ✅ Tool calling
- ✅ Graph-based orchestration

### Production Considerations
- ✅ Async/await patterns
- ✅ Error resilience
- ✅ Session management
- ✅ Tool safety

## Notes

- All examples use **Gemini 2.5 Flash** model
- Examples are self-contained (no external dependencies beyond LangChain)
- Each example demonstrates specific concepts clearly
- Code is commented for educational purposes
- All examples use `load_dotenv()` for API key management

## Next Steps

After completing these examples, students should:
1. Experiment with different models and parameters
2. Build their own RAG systems
3. Create custom tools for agents
4. Design graph-based workflows
5. Implement production patterns (caching, monitoring, etc.)

