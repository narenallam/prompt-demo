"""
LangChain Example 4: Runnables & LCEL Advanced Patterns
Demonstrates branching, mapping, streaming, and error handling.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnablePassthrough, RunnableLambda
from langchain_core.exceptions import OutputParserException
from langchain_google_genai import ChatGoogleGenerativeAI
import random

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

# Example 1: Branching & Mapping with RunnableMap
print("="*80)
print("Example 1: Branching & Mapping with RunnableMap")
print("="*80)

prompt1 = ChatPromptTemplate.from_template("Translate to French: {text}")
prompt2 = ChatPromptTemplate.from_template("Summarize in 5 words: {text}")

# This chain will take an input {"text": ...}
# and run two branches in parallel.
map_chain = RunnableMap({
    "french": prompt1 | model | parser,
    "summary": prompt2 | model | parser
})

result = map_chain.invoke({"text": "LangChain 1.0 introduces Runnables and LCEL for composability."})
print(f"\nParallel Results:\n{result}")

# Example 2: Streaming
print("\n" + "="*80)
print("Example 2: Streaming")
print("="*80)

prompt_stream = ChatPromptTemplate.from_template("Write a 3-line haiku about composable AI.")
chain_stream = prompt_stream | model | parser

print("\n--- Invoking (Full Response) ---")
print(chain_stream.invoke({}))

print("\n--- Streaming (Token by Token) ---")
for token in chain_stream.stream({}):
    print(token, end="", flush=True)
print()

# Example 3: Error Handling and Retries
print("\n" + "="*80)
print("Example 3: Error Handling and Retries")
print("="*80)

# Track attempts for demonstration
attempt_count = [0]

def risky_parser(message):
    """A parser that fails on first attempt, succeeds on retry."""
    attempt_count[0] += 1
    # Extract content from message if it's an AIMessage
    if hasattr(message, 'content'):
        text = message.content
    else:
        text = str(message)
    
    # Fail on first attempt, succeed on retry
    if attempt_count[0] == 1:
        print(f"-> PARSER FAILED (attempt {attempt_count[0]})")
        raise OutputParserException("Simulated random failure!")
    print(f"-> PARSER SUCCEEDED (attempt {attempt_count[0]})")
    return text.strip()

# Wrap the risky function in a RunnableLambda
# and attach a retry mechanism.
safe_parser = RunnableLambda(risky_parser).with_retry(
    stop_after_attempt=3,  # Retry up to 3 times
    wait_exponential_jitter=False  # Use simple backoff
)

prompt_retry = ChatPromptTemplate.from_template("Say hello in one word.")
chain_retry = prompt_retry | model | safe_parser

print("\nTesting retry mechanism:")
attempt_count[0] = 0  # Reset counter
result = chain_retry.invoke({})
print(f"Final result: {result}")

