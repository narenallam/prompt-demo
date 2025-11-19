"""
LangChain Example 6: Memory Systems
Demonstrates conversation memory with RunnableWithMessageHistory.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage

# Simple in-memory chat history
class ChatMessageHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []
    
    def add_message(self, message: BaseMessage):
        self.messages.append(message)
    
    def clear(self):
        self.messages = []

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),  # This is where history is injected
    ("human", "{input}"),
])

chain = prompt | llm

# In-memory store for this session
session_history = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """Gets the history for a given session_id."""
    if session_id not in session_history:
        session_history[session_id] = ChatMessageHistory()
    return session_history[session_id]

# Wrap the chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print("="*80)
print("Memory Systems: Multi-User Conversation")
print("="*80)

# --- Run for User 1 ---
print("\n--- User 1 ---")
config_user_1 = {"configurable": {"session_id": "user123"}}
response = chain_with_memory.invoke({"input": "My name is Alice"}, config=config_user_1)
print(f"AI: {response.content}")

response = chain_with_memory.invoke({"input": "What is my name?"}, config=config_user_1)
print(f"AI: {response.content}")

# --- Run for User 2 ---
print("\n--- User 2 ---")
config_user_2 = {"configurable": {"session_id": "user456"}}
response = chain_with_memory.invoke({"input": "My name is Bob"}, config=config_user_2)
print(f"AI: {response.content}")

# --- User 1 Again ---
print("\n--- User 1 (Again) ---")
response = chain_with_memory.invoke({"input": "What's my name again?"}, config=config_user_1)
print(f"AI: {response.content}")  # It remembers "Alice"

