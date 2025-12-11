"""
LangChain Example 1: Hello LangChain 1.0 (LCEL)
Demonstrates the power and simplicity of LCEL with the pipe operator.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Define the components
prompt = ChatPromptTemplate.from_template(
    "Translate the following text to French: {text}"
)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

# 2. Compose the chain using the | (pipe) operator
chain = prompt | model | parser

# 3. Invoke the chain
result = chain.invoke({"text": "Good morning"})
print(f"Translation: {result}")

# # Example 2: Sync and Async invocation
# print("\n" + "=" * 80)
# print("Example 2: Sync and Async Invocation")
# print("=" * 80)

# prompt2 = ChatPromptTemplate.from_template(
#     "Rewrite this text in one concise sentence: {text}"
# )
# model2 = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# chain2 = prompt2 | model2 | parser

# # Sync invocation
# print("\n--- SYNC ---")
# sync_result = chain2.invoke(
#     {
#         "text": "I wanted to tell you some thing yesterday, which I could'not tell you, but im planning to tell you"
#     }
# )
# print(f"Sync Result: {sync_result}")

# # # Async invocation
# import asyncio


# async def run_async():
#     print("\n--- ASYNC ---")
#     async_result = await chain2.ainvoke(
#         {
#             "text": "LCEL enables concise, type-safe composition and automatically supports streaming."
#         }
#     )
#     print(f"Async Result: {async_result}")


# asyncio.run(run_async())
