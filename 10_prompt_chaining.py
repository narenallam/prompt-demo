"""
LangChain Example 10: Chain-Of-Thought with Self-Reflection / Self-Critique Pattern
Demonstrates using the LLM to improve its own output: Draft -> Critique -> Revise.
Uses Ollama with llama3.1:8b model running locally.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0)

draft_prompt = ChatPromptTemplate.from_template(
    "Provide a concise answer to: {question}"
)

critique_prompt = ChatPromptTemplate.from_template(
    """Critique the following answer based on these criteria:
1. Is it correct?
2. Is it concise?
Suggest concrete improvements.

ANSWER:
{draft}
"""
)

revise_prompt = ChatPromptTemplate.from_template(
    """Revise the original answer based on the provided critique.

ORIGINAL QUESTION: {question}
ORIGINAL ANSWER: {draft}
CRITIQUE: {critique}

REVISED ANSWER:
"""
)

# Define the chains
draft_chain = draft_prompt | llm | StrOutputParser()
critique_chain = critique_prompt | llm | StrOutputParser()
revise_chain = revise_prompt | llm | StrOutputParser()

# Define the question
question = "Explain attention mechanism in LLMs, in two lines"

print("="*80)
print("Self-Reflection Pattern: Draft -> Critique -> Revise")
print("="*80)
print(f"\nQuestion: {question}\n")

# Step 1: Generate initial draft
print("-" * 80)
print("STEP 1: DRAFT")
print("-" * 80)
draft = draft_chain.invoke({"question": question})
print(draft)

# Step 2: Critique the draft
print("\n" + "-" * 80)
print("STEP 2: CRITIQUE")
print("-" * 80)
critique = critique_chain.invoke({"draft": draft})
print(critique)

# Step 3: Revise based on critique
print("\n" + "-" * 80)
print("STEP 3: REVISED ANSWER")
print("-" * 80)
revised = revise_chain.invoke({
    "question": question,
    "draft": draft,
    "critique": critique
})
print(revised)

print("\n" + "="*80)

