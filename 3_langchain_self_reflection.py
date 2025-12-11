# LangChain Example 3: Chain-Of-Thought with Self-Reflection / Self-Critique
# Pattern Demonstrates using the LLM to improve its own output: Draft ->
# Critique -> Revise.

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

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

# Define the data flow using RunnablePassthrough
# 1. Run the draft chain and add 'draft' to input dict
# 2. Run the critique chain and add 'critique' to input dict
# 3. Pass all three (draft, question, critique) to the revise chain
# RunnablePassthrough automatically preserves existing keys
# while adding new ones

pipeline = (
    RunnablePassthrough.assign(draft=draft_chain)
    | RunnablePassthrough.assign(critique=critique_chain)
    | revise_chain
)

print("=" * 80)
print("Self-Reflection Pattern: Draft -> Critique -> Revise")
print("=" * 80)

result = pipeline.invoke(
    {"question": "Explain attention mechanism in LLMs, in two lines"}
)
print(f"\nFinal Revised Answer:\n{result}")
