"""
LangChain Example 6: Memory Systems (LangChain 1.0+ Compatible)

IMPORTANT: Runnables ARE The Modern LangChain 1.0+ Standard!
============================================================
 Runnables are the CORE abstraction in LangChain 1.0+
 RunnableWithMessageHistory is the RECOMMENDED memory approach
 OLD: ConversationBufferMemory, ConversationSummaryMemory (DEPRECATED)
 NEW: RunnableWithMessageHistory + custom history implementations

MEMORY STRATEGIES DEMONSTRATED:
================================
1. Simple In-Memory History (this example)
2. Windowed Memory (last N messages)
3. Summary-Based Memory (for long conversations)

USE CASES:
==========
- Multi-user chat applications (session per user)
- Customer support bots (maintain context per customer)
- Personal assistants (remember user preferences)
- Educational tutors (track learning progress)
"""

from typing import List

from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# ============================================================================
# MEMORY STRATEGY 1: Simple In-Memory History
# ============================================================================
# Stores ALL messages - good for short conversations
# Use case: Quick customer support interactions, simple Q&A


class ChatMessageHistory(BaseChatMessageHistory):
    """Stores all conversation messages in memory."""

    def __init__(self):
        self.messages: List[BaseMessage] = []

    def add_message(self, message: BaseMessage):
        """Add a message to the history."""
        self.messages.append(message)

    def clear(self):
        """Clear all messages."""
        self.messages = []


# ============================================================================
# MEMORY STRATEGY 2: Windowed History (Last N Messages)
# ============================================================================
# Keeps only the last N messages to prevent context overflow
# Use case: Long conversations, chat apps with token limits


class WindowedChatMessageHistory(BaseChatMessageHistory):
    """Keeps only the last 'window_size' messages."""

    def __init__(self, window_size: int = 10):
        self.messages: List[BaseMessage] = []
        self.window_size = window_size

    def add_message(self, message: BaseMessage):
        """Add message and maintain window size."""
        self.messages.append(message)
        # Keep only last N messages
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size :]

    def clear(self):
        """Clear all messages."""
        self.messages = []


# ============================================================================
# SETUP: Create LLM and Prompt Template
# ============================================================================
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# This prompt uses MessagesPlaceholder for dynamic history injection
# This is the LangChain 1.0+ pattern (Runnable-based)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),  # History injected here
        ("human", "{input}"),
    ]
)

# Create the base chain using LCEL (LangChain Expression Language)
chain = prompt | llm


# ============================================================================
# EXAMPLE 1: Basic Multi-Session Memory
# ============================================================================
# Use case: Multi-user chat app where each user has their own history
print("\n" + "=" * 80)
print("EXAMPLE 1: Multi-Session Memory (Different Users)")
print("=" * 80)

# Session store: maps session_id -> ChatMessageHistory
session_store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    """Factory function to get or create session history."""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


# Wrap chain with memory using RunnableWithMessageHistory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# User 1's conversation
print("\n User 1 (Alice):")
config_user_1 = {"configurable": {"session_id": "user123"}}
response = chain_with_memory.invoke({"input": "My name is Alice"}, config=config_user_1)
print(f"   AI: {response.content}")

response = chain_with_memory.invoke({"input": "What is my name?"}, config=config_user_1)
print(f"   AI: {response.content}")

# User 2's separate conversation
print("\n User 2 (Bob):")
config_user_2 = {"configurable": {"session_id": "user456"}}
response = chain_with_memory.invoke({"input": "My name is Bob"}, config=config_user_2)
print(f"   AI: {response.content}")

# User 1 again - memory persists
print("\n User 1 (Alice) returns:")
response = chain_with_memory.invoke(
    {"input": "What's my name again?"}, config=config_user_1
)
print(f"   AI: {response.content}")  # Remembers "Alice"!


# ============================================================================
# EXAMPLE 2: Windowed Memory (Last N Messages)
# ============================================================================
# Use case: Long conversations where you want to limit context
print("\n\n" + "=" * 80)
print("EXAMPLE 2: Windowed Memory (Last 4 Messages Only)")
print("=" * 80)

windowed_store = {}


def get_windowed_history(session_id: str) -> WindowedChatMessageHistory:
    """Get windowed history (keeps only last 4 messages)."""
    if session_id not in windowed_store:
        windowed_store[session_id] = WindowedChatMessageHistory(window_size=4)
    return windowed_store[session_id]


chain_with_window = RunnableWithMessageHistory(
    chain,
    get_windowed_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "long_conversation"}}

# Simulate a long conversation
messages = [
    "My favorite color is blue",
    "My favorite food is pizza",
    "My favorite hobby is reading",
    "My favorite movie is Inception",
]

print("\n Sending multiple messages:")
for msg in messages:
    response = chain_with_window.invoke({"input": msg}, config=config)
    print(f"  Human: {msg}")
    print(f"   AI: {response.content}\n")

# Ask about earlier info (should remember only recent items)
print(" Testing memory window:")
response = chain_with_window.invoke(
    {"input": "What's my favorite color?"}, config=config
)
print("  Human: What's my favorite color?")
print(f"   AI: {response.content}")
print("  ℹ  May not remember if it's outside the window!\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "=" * 80)
print("KEY TAKEAWAYS - LangChain 1.0+ Memory")
print("=" * 80)
print(
    """
 MODERN APPROACH (LangChain 1.0+):
   - RunnableWithMessageHistory (Runnable-based)
   - Custom BaseChatMessageHistory implementations
   - Session-based memory with configurable IDs

 DEPRECATED (Don't use in new code):
   - ConversationBufferMemory
   - ConversationSummaryMemory
   - ConversationBufferWindowMemory
   - All langchain.memory.* classes

 WHEN TO USE WHICH STRATEGY:
   1. Simple History: Short conversations, full context needed
   2. Windowed History: Long chats, token limits, recent context
   3. Summary-Based: Very long conversations (implement custom)

 PRODUCTION TIPS:
   - Store history in database (Redis, PostgreSQL, etc.)
   - Implement custom BaseChatMessageHistory for persistence
   - Use session IDs tied to user IDs or conversation IDs
   - Consider token limits when designing memory strategy

 FOR STATEFUL APPS WITH COMPLEX WORKFLOWS:
   - Use LangGraph with MemorySaver/checkpointing
   - See: 8_langchain_langgraph.py for examples
"""
)

print("=" * 80)
print(" All examples completed successfully!")
print("=" * 80)
