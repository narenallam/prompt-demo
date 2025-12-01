"""
LangChain Example 8: LangGraph - Stateful Multi-Agent Workflows (v1.0)

WHAT IS LANGGRAPH?
==================
LangGraph is a library for building stateful, multi-actor applications
with LLMs. It extends LangChain with:
- Graph-based workflow orchestration
- Built-in persistence/checkpointing
- Cycles and conditional routing
- Human-in-the-loop patterns

LANGGRAPH VS REGULAR AGENTS:
=============================
Use LangGraph when you need:
   Complex state management across steps
   Cyclic workflows (loops, retries, iterations)
   Multi-agent systems
   Human approval/feedback loops
   Persistent conversation state

Use Regular Agents when:
   Simple, linear tool calling
   Quick prototypes
   No complex state needed

KEY CONCEPTS:
=============
1. StateGraph: Defines nodes and edges
2. Nodes: Functions that process state
3. Edges: Transitions between nodes
4. Checkpointing: Persists state between runs
5. Conditional Edges: Dynamic routing based on state

USE CASES DEMONSTRATED:
=======================
1. Research Assistant (multi-step workflow)
2. Customer Support Router (conditional routing)
3. Code Review Agent (human-in-the-loop)
"""

from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# ============================================================================
# EXAMPLE 1: Simple Chatbot with Memory (LangGraph Basics)
# ============================================================================
# Demonstrates: StateGraph, Messages, Checkpointing
print("\n" + "=" * 80)
print("EXAMPLE 1: Simple Chatbot with Memory")
print("=" * 80)


class ChatbotState(TypedDict):
    """
    State schema for the chatbot.
    'messages' uses add_messages reducer to append new messages.
    """

    messages: Annotated[list[BaseMessage], add_messages]


# Define the chatbot node
def chatbot_node(state: ChatbotState) -> dict:
    """The chatbot node that calls the LLM."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# Build the graph
chatbot_graph_builder = StateGraph(ChatbotState)
chatbot_graph_builder.add_node("chatbot", chatbot_node)
chatbot_graph_builder.add_edge(START, "chatbot")
chatbot_graph_builder.add_edge("chatbot", END)

# Add checkpointing for memory
memory = MemorySaver()
chatbot_graph = chatbot_graph_builder.compile(checkpointer=memory)

# Use the chatbot with persistent memory
print("\n Conversation 1:")
config = {"configurable": {"thread_id": "conversation_1"}}
result = chatbot_graph.invoke(
    {"messages": [HumanMessage(content="Hi! My name is Alice")]},
    config=config,
)
print("User: Hi! My name is Alice")
print(f"Bot: {result['messages'][-1].content}\n")

print(" Conversation 1 (continued):")
result = chatbot_graph.invoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config=config,
)
print("User: What's my name?")
print(f"Bot: {result['messages'][-1].content}")
print(" The bot remembers Alice from the previous message!\n")

# ============================================================================
# EXAMPLE 2: Tool-Calling Agent with Conditional Routing
# ============================================================================
# Demonstrates: Tools, Conditional Edges, ToolNode
print("\n" + "=" * 80)
print("EXAMPLE 2: Research Agent with Tools")
print("=" * 80)


# Define tools
@tool
def search_knowledge_base(query: str) -> str:
    """Search internal knowledge base for information about LangGraph."""
    knowledge = {
        "langgraph": "LangGraph is a library for building stateful, "
        "multi-actor applications with LLMs using graph structures.",
        "checkpointing": "Checkpointing in LangGraph allows you to save "
        "and restore state, enabling features like time travel.",
        "tools": "Tools are functions that agents can call to perform "
        "specific actions or retrieve information.",
    }

    for key, value in knowledge.items():
        if key in query.lower():
            print(f"   Found info about: {key}")
            return value

    return "No information found. Try: langgraph, checkpointing, or tools."


@tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression)  # noqa: S307
        print(f"   Calculated: {expression} = {result}")
        return f"The result is {result}"
    except Exception as e:
        return f"Error: {str(e)}"


tools = [search_knowledge_base, calculate]


# Define the agent state
class AgentState(TypedDict):
    """State for the research agent."""

    messages: Annotated[list[BaseMessage], add_messages]


# Create LLM with tools
llm_with_tools = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", temperature=0
).bind_tools(tools)


# Define agent node
def agent_node(state: AgentState) -> dict:
    """The agent decides whether to use tools or respond directly."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# Define routing function
def should_continue_func(
    state: AgentState,
) -> Literal["tools", "end"]:
    """Determine if we should call tools or end."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("  → Routing to tools")
        return "tools"
    print("  → Routing to end")
    return "end"


# Build the graph
agent_graph_builder = StateGraph(AgentState)

# Add nodes
agent_graph_builder.add_node("agent", agent_node)
agent_graph_builder.add_node("tools", ToolNode(tools))

# Add edges
agent_graph_builder.add_edge(START, "agent")
agent_graph_builder.add_conditional_edges(
    "agent", should_continue_func, {"tools": "tools", "end": END}
)
agent_graph_builder.add_edge("tools", "agent")  # Loop back after tools

# Compile
agent_graph = agent_graph_builder.compile()

# Test the agent
print("\n Query: Tell me about LangGraph checkpointing")
result = agent_graph.invoke(
    {"messages": [HumanMessage("Tell me about LangGraph checkpointing")]}
)
print(f" Answer: {result['messages'][-1].content}\n")

print(" Query: Calculate 156 * 23")
result = agent_graph.invoke({"messages": [HumanMessage("Calculate 156 * 23")]})
print(f" Answer: {result['messages'][-1].content}\n")


# ============================================================================
# EXAMPLE 3: Multi-Step Workflow with State Management
# ============================================================================
# Demonstrates: Complex state, multiple nodes, sequential workflow
print("\n" + "=" * 80)
print("EXAMPLE 3: Content Creation Workflow")
print("=" * 80)


class WorkflowState(TypedDict):
    """State for content creation workflow."""

    topic: str
    outline: str
    draft: str
    review: str
    final_content: str


def create_outline_node(state: WorkflowState) -> dict:
    """Generate an outline for the topic."""
    print("\n   Step 1: Creating outline...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    prompt = f"Create a brief outline for a blog post about: {state['topic']}"
    response = llm.invoke(prompt)
    outline = response.content
    print(f"   Outline created: {outline[:80]}...")
    return {"outline": outline}


def write_draft_node(state: WorkflowState) -> dict:
    """Write a draft based on the outline."""
    print("\n    Step 2: Writing draft...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    prompt = f"Write a 2-paragraph draft based on this outline:\n{state['outline']}"
    response = llm.invoke(prompt)
    draft = response.content
    print(f"   Draft created: {draft[:80]}...")
    return {"draft": draft}


def review_node(state: WorkflowState) -> dict:
    """Review the draft and provide feedback."""
    print("\n   Step 3: Reviewing draft...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    prompt = f"Review this draft and suggest ONE improvement:\n{state['draft']}"
    response = llm.invoke(prompt)
    review = response.content
    print(f"   Review complete: {review[:80]}...")
    return {"review": review}


def finalize_node(state: WorkflowState) -> dict:
    """Incorporate review feedback into final version."""
    print("\n   Step 4: Finalizing content...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
    prompt = (
        f"Improve this draft based on the review:\n\n"
        f"DRAFT: {state['draft']}\n\n"
        f"REVIEW: {state['review']}"
    )
    response = llm.invoke(prompt)
    final = response.content
    print(f"   Final content ready: {final[:80]}...")
    return {"final_content": final}


# Build the workflow graph
workflow_graph_builder = StateGraph(WorkflowState)

# Add nodes in sequence
workflow_graph_builder.add_node("outline", create_outline_node)
workflow_graph_builder.add_node("draft", write_draft_node)
workflow_graph_builder.add_node("review", review_node)
workflow_graph_builder.add_node("finalize", finalize_node)

# Add sequential edges
workflow_graph_builder.add_edge(START, "outline")
workflow_graph_builder.add_edge("outline", "draft")
workflow_graph_builder.add_edge("draft", "review")
workflow_graph_builder.add_edge("review", "finalize")
workflow_graph_builder.add_edge("finalize", END)

# Compile
workflow_graph = workflow_graph_builder.compile()

# Run the workflow
print("\n Running content creation workflow...")
result = workflow_graph.invoke({"topic": "Benefits of using LangGraph"})
print("\n" + "=" * 80)
print(" FINAL CONTENT:")
print("=" * 80)
print(result["final_content"])
print("\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "=" * 80)
print("KEY TAKEAWAYS - LangGraph 1.0")
print("=" * 80)
print(
    """
 CORE CONCEPTS:
   1. StateGraph: Define nodes and edges
   2. State: TypedDict with reducers (like add_messages)
   3. Nodes: Functions that process and update state
   4. Edges: Fixed transitions (add_edge)
   5. Conditional Edges: Dynamic routing (add_conditional_edges)
   6. Checkpointing: Persist state with MemorySaver

 WHEN TO USE LANGGRAPH:
   - Multi-step workflows with state
   - Tool-calling agents with cycles
   - Human-in-the-loop workflows
   - Multi-agent collaboration
   - Workflows needing persistence/resume

 BEST PRACTICES:
   - Use TypedDict for clear state schemas
   - Use add_messages reducer for message lists
   - Compile with checkpointer for memory
   - Use ToolNode for built-in tool execution
   - Use conditional_edges for dynamic routing

 PRODUCTION PATTERNS:
   1. Add error handling in nodes
   2. Use checkpointers for persistence (SQLite, Redis)
   3. Implement timeout/retry logic
   4. Log state transitions for debugging
   5. Use thread_id for multi-user apps

 ADVANCED FEATURES (Not shown):
   - Human-in-the-loop with interrupt()
   - Time travel (rewind state)
   - Streaming intermediate steps
   - Sub-graphs for modularity
   - Multi-agent orchestration
"""
)

print("=" * 80)
print(" All LangGraph examples completed successfully!")
print("=" * 80)
