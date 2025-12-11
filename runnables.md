# LangChain Runnables: Complete Guide

## What are Runnables?

**Runnables** are LangChain's building blocks for creating composable AI pipelines. They all implement a standard interface:
- `.invoke()` - synchronous execution
- `.stream()` - streaming output
- `.batch()` - batch processing
- `.ainvoke()`, `.astream()`, `.abatch()` - async versions

## Core Runnable Types

### 1. **`RunnablePassthrough`** - Pass data through, optionally adding fields

**When to use**: Preserve input values while adding new computed fields

```python
from langchain_core.runnables import RunnablePassthrough

# Basic: Pass input through unchanged
chain = RunnablePassthrough() | some_chain

# With assign: Add new fields while keeping existing ones
chain = (
    RunnablePassthrough.assign(draft=draft_chain)      # adds 'draft'
    | RunnablePassthrough.assign(critique=critique_chain)  # adds 'critique'
    | final_chain  # receives all fields: original + draft + critique
)

# Input: {"question": "..."}
# After first assign: {"question": "...", "draft": "..."}
# After second assign: {"question": "...", "draft": "...", "critique": "..."}
```

**Use cases**:
- Self-reflection patterns (draft → critique → revise)
- Multi-step enrichment pipelines
- Keeping context as you add computed values

---

### 2. **`RunnableMap`** - Execute multiple branches in parallel

**When to use**: Run independent operations simultaneously on the same input

```python
from langchain_core.runnables import RunnableMap

# Execute french translation AND summary at the same time
map_chain = RunnableMap({
    "french": prompt1 | model | parser,
    "summary": prompt2 | model | parser,
    "word_count": lambda x: len(x["text"].split())
})

# Input: {"text": "..."}
# Output: {"french": "...", "summary": "...", "word_count": 42}
```

**Use cases**:
- Generate multiple outputs from same input (translate + summarize)
- Compare different models/prompts side-by-side
- Parallel data enrichment (sentiment + entities + summary)
- Speed optimization (2x faster than sequential)

**Key**: All branches execute **concurrently** (async parallel execution)

---

### 3. **`RunnableLambda`** - Wrap custom Python functions

**When to use**: Add custom logic, preprocessing, or postprocessing to chains

```python
from langchain_core.runnables import RunnableLambda

# Simple function wrapper
def extract_json(text):
    import json
    return json.loads(text)

parser = RunnableLambda(extract_json)

# In a chain
chain = prompt | model | RunnableLambda(extract_json) | process_data

# With retry logic
safe_parser = RunnableLambda(risky_function).with_retry(
    stop_after_attempt=3
)

# Async function support
async def async_api_call(data):
    async with httpx.AsyncClient() as client:
        return await client.post("...", json=data)

chain = preprocessor | RunnableLambda(async_api_call) | postprocessor
```

**Use cases**:
- Custom parsing/validation logic
- API calls to external services
- Data transformation between chain steps
- Adding retry/error handling (`.with_retry()`)
- Logging and debugging

---

### 4. **`RunnableParallel`** - Alias for `RunnableMap`

```python
from langchain_core.runnables import RunnableParallel

# Same as RunnableMap - more explicit name
parallel_chain = RunnableParallel(
    translation=translate_chain,
    summary=summary_chain
)
```

**When to use**: Use when you want to emphasize parallel execution (personal preference)

---

### 5. **`RunnableBranch`** - Conditional routing

**When to use**: Route to different chains based on conditions

```python
from langchain_core.runnables import RunnableBranch

# Route based on input type
branch = RunnableBranch(
    (lambda x: x["type"] == "question", qa_chain),
    (lambda x: x["type"] == "summarize", summary_chain),
    default_chain  # fallback
)

# Input: {"type": "question", "text": "..."}
# Routes to qa_chain
```

**Use cases**:
- Different handling for different input types
- Multi-intent chatbots (question vs command vs chitchat)
- Dynamic prompt selection

---

### 6. **`RunnableSequence`** - Sequential chaining (rarely used directly)

**When to use**: Created automatically with `|` operator

```python
# These are equivalent:
chain = prompt | model | parser
chain = RunnableSequence(first=prompt, middle=[model], last=parser)

# Just use | operator - don't create RunnableSequence directly
```

**Note**: You almost never create this manually—use `|` instead

---

### 7. **`RunnableWithFallbacks`** - Fallback to alternative chains

**When to use**: Graceful degradation when primary chain fails

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Try GPT-4, fall back to Gemini if it fails
primary = ChatOpenAI(model="gpt-4")
fallback = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chain = (prompt | primary | parser).with_fallbacks([fallback])
```

**Use cases**:
- Multi-provider redundancy (OpenAI fails → use Gemini)
- Expensive model → cheaper fallback
- Complex chain → simpler backup

---

### 8. **`RunnableGenerator`** - Custom streaming logic

**When to use**: Create custom streaming implementations

```python
from langchain_core.runnables import RunnableGenerator

def custom_streamer(input_stream):
    for chunk in input_stream:
        # Custom processing
        yield process_chunk(chunk)

streaming_chain = RunnableGenerator(custom_streamer)
```

**Use cases**: Advanced streaming customization (rare)

---

## Quick Decision Tree

```
Need to preserve input while adding fields?
  → RunnablePassthrough.assign()

Need multiple operations on same input simultaneously?
  → RunnableMap / RunnableParallel

Need custom Python function in chain?
  → RunnableLambda

Need conditional routing?
  → RunnableBranch

Need fallback when chain fails?
  → .with_fallbacks()

Need to chain operations sequentially?
  → Use | operator (creates RunnableSequence automatically)
```

---

## Real-World Example Combining Multiple Runnables

```python
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableMap,
    RunnableLambda,
    RunnableBranch
)

# 1. Parallel analysis
analysis = RunnableMap({
    "sentiment": sentiment_prompt | model | parser,
    "entities": entity_prompt | model | parser,
    "summary": summary_prompt | model | parser
})

# 2. Custom scoring
def calculate_score(data):
    # Custom logic
    return {**data, "score": len(data["entities"]) * 0.5}

# 3. Conditional routing based on score
router = RunnableBranch(
    (lambda x: x["score"] > 5, detailed_response_chain),
    (lambda x: x["score"] > 2, standard_response_chain),
    brief_response_chain
)

# Complete pipeline
pipeline = (
    RunnablePassthrough.assign(analysis=analysis)  # add parallel analysis
    | RunnableLambda(calculate_score)              # add score
    | router                                        # route based on score
)

# Input: {"text": "..."}
# Output: Detailed/standard/brief response based on analysis
```

---

## Summary Table

| Runnable | Purpose | Execution | Common Use |
|----------|---------|-----------|------------|
| `RunnablePassthrough` | Pass data through + optional fields | Sequential | Preserve context |
| `RunnableMap` | Multiple branches | **Parallel** | Multi-output generation |
| `RunnableLambda` | Custom function | Sequential | Custom logic |
| `RunnableBranch` | Conditional routing | Sequential | If/else logic |
| `RunnableSequence` | Chain steps | Sequential | Auto-created by `\|` |
| `.with_fallbacks()` | Backup chains | Sequential | Error handling |

**Key insight**: Only `RunnableMap`/`RunnableParallel` execute in parallel—everything else is sequential!