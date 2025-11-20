"""
LangChain Example 2: Core Prompt Engineering Techniques
Demonstrates role prompting, zero-shot, few-shot, chain-of-thought, and structural prompting.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

# # Example 1: Role Prompting (System Prompts)
# print("="*80)
# print("Example 1: Role Prompting (System Prompts)")
# print("="*80)

# prompt_role = ChatPromptTemplate.from_template("Write a short product tagline for: {idea}")

# # Deterministic model for factual tasks
# llm_strict = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0
# )

# # Creative model for brainstorming
# llm_creative = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=1.5
# )

# chain_strict = prompt_role | llm_strict | parser
# chain_creative = prompt_role | llm_creative | parser

# idea = {"idea": "a privacy-first note-taking app"}
# print(f"\nStrict: {chain_strict.invoke(idea)}")
# print(f"Creative: {chain_creative.invoke(idea)}")

# # Example 2: System Message Role
# print("\n" + "="*80)
# print("Example 2: System Message Role")
# print("="*80)

# prompt_messages = [
#     SystemMessage(
#         content="You are a helpful assistant who translates English to French. "
#         "You only reply with the French translation and nothing else."
#     ),
#     HumanMessage(content="Hello, how are you?"),
# ]

# response = model.invoke(prompt_messages)
# print(f"Translation: {response.content}")

# Example 3: Few-Shot Prompting
# print("\n" + "="*80)
# print("Example 3: Few-Shot Prompting")
# print("="*80)

# few_shot_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a sentiment classifier. Respond with POSITIVE, NEGATIVE, or NEUTRAL."),
#     # --- Examples ---
#     ("human", "This new update is amazing!"),
#     ("ai", "POSITIVE"),
#     ("human", "I'm not sure if I like this design."),
#     ("ai", "NEUTRAL"),
#     ("human", "The app keeps crashing."),
#     ("ai", "NEGATIVE"),
#     # --- End Examples ---
#     ("human", "{text_to_classify}"),
# ])

# classifier_chain = few_shot_prompt | model | parser
# result = classifier_chain.invoke({"text_to_classify": "I'm skeptical about the success of the movie"})
# print(f"Sentiment: {result}")

# Example 4: Chain-of-Thought (CoT) Prompting
print("\n" + "="*80)
print("Example 4: Chain-of-Thought (CoT) Prompting")
print("="*80)

# Bad "Direct" Prompt
prompt_direct = ChatPromptTemplate.from_template(
    "Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
    "Each can has 3 tennis balls. How many tennis balls does he have now?\n"
    "A:"
)

# Good "CoT" Prompt
prompt_cot = ChatPromptTemplate.from_template(
    "Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
    "Each can has 3 tennis balls. How many tennis balls does he have now?\n"
    "A: Let's think step by step.\n"
    "1. Roger starts with 5 balls.\n"
    "2. He buys 2 cans of balls.\n"
    "3. Each can has 3 balls, so 2 cans have 2 * 3 = 6 balls.\n"
    "4. In total, he has 5 (initial) + 6 (new) = 11 balls.\n"
    "The final answer is 11."
)

# You can also prompt it to *generate* the steps:
prompt_cot_generate = ChatPromptTemplate.from_template(
    "Q: {question}\n"
    "A: Let's think step by step."
)

cot_chain = prompt_cot_generate | model | parser
# result = cot_chain.invoke({"question": "A store has 20 apples. They sell 8 in the morning and 5 in the afternoon. How many are left?"})
result = cot_chain.invoke({"question": '''Mr Rao, usually picks his son from the school
 everyday evening. One day school closed earlier, his son did not wait at the schol,
 instead he walks towards home. Mr Rao started to pick his son in usual time, 
 but found his son on the way to home, and returned back with him, 
 on that day he arrived the home 15 mins earlier. What is the distance 
 between his school and the home?. Think step-by-step and come to the answer'''})
print(f"CoT Answer:\n{result}")

# Example 5: Structural Prompting (XML Tags)
print("\n" + "="*80)
print("Example 5: Structural Prompting (XML Tags)")
print("="*80)

prompt_xml = ChatPromptTemplate.from_template(
    "Extract the key information from the following text. "
    "Return your answer inside <response> XML tags. "
    "Provide a <title> and a <summary_points> list with <point> tags.\n\n"
    "<text>{text_input}</text>\n\n"
    "<response>"
)

xml_chain = prompt_xml | model | parser
result = xml_chain.invoke({"text_input": "LangChain 1.0 introduces LCEL for composable AI pipelines. It supports streaming, async, and automatic retries."})
print(f"XML Structured Output:\n{result}")

