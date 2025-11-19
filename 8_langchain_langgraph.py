"""
LangChain Example 8: LangGraph Concepts - Stateful, Cyclic Applications
Demonstrates graph-based orchestration concepts (simplified implementation).
Note: Full LangGraph requires: pip install langgraph
"""

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

# Example 1: Stateful Counter (Conceptual LangGraph Pattern)
print("="*80)
print("Example 1: Stateful Counter (Conceptual Pattern)")
print("="*80)

class CounterState(TypedDict):
    """The state for our counter graph."""
    count: int

def add_one(state: CounterState) -> Dict[str, int]:
    """A node that increments the count."""
    print(f"Node: add_one. Current count: {state['count']}")
    return {"count": state['count'] + 1}

def subtract_one(state: CounterState) -> Dict[str, int]:
    """A node that decrements the count."""
    print(f"Node: subtract_one. Current count: {state['count']}")
    return {"count": state['count'] - 1}

# Simple graph execution (simulating LangGraph)
def run_counter_graph(initial_state: CounterState, steps: int = 5):
    """Simulates a graph execution."""
    state = initial_state.copy()
    for i in range(steps):
        if i % 2 == 0:
            state = add_one(state)
        else:
            state = subtract_one(state)
        print(f"State after step {i+1}: {state}")
    return state

result = run_counter_graph({"count": 0}, steps=5)
print(f"\nFinal state: {result}")

# Example 2: Agentic Router Pattern (Conceptual)
print("\n" + "="*80)
print("Example 2: Agentic Router with Tools (Conceptual Pattern)")
print("="*80)

@tool
def search_web(query: str) -> str:
    """Searches the web for relevant information."""
    print(f"--- Calling Search Tool: {query} ---")
    return f"Search results for '{query}': LangGraph is for cyclic graphs."

tools = [search_web]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash").bind_tools(tools)

class AgentState(TypedDict):
    messages: List[BaseMessage]
    iteration: int

def call_model(state: AgentState) -> Dict[str, Any]:
    """The 'agent' node. Calls the LLM."""
    response = llm.invoke(state["messages"])
    return {
        "messages": state["messages"] + [response],
        "iteration": state["iteration"] + 1
    }

def call_tool(state: AgentState) -> Dict[str, Any]:
    """The 'tool' node. Executes tools."""
    last_message = state["messages"][-1]
    
    # Check for tool calls (simplified - actual implementation would parse tool_calls properly)
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]
        tool_name = tool_call.get("name", "")
        tool_args = tool_call.get("args", {})
        
        if tool_name == "search_web":
            result = search_web.invoke(tool_args)
            tool_message = ToolMessage(
                content=str(result),
                tool_call_id=tool_call.get("id", "1")
            )
            return {
                "messages": state["messages"] + [tool_message],
                "iteration": state["iteration"]
            }
    
    return state

def should_continue(state: AgentState) -> str:
    """The router. Decides the next step."""
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tool"
    else:
        return "end"

# Simple graph execution
def run_agent_graph(query: str, max_iterations: int = 5):
    """Simulates an agent graph execution."""
    state: AgentState = {
        "messages": [HumanMessage(content=query)],
        "iteration": 0
    }
    
    for i in range(max_iterations):
        print(f"\n[Iteration {i+1}]")
        
        # Agent node
        state = call_model(state)
        print(f"Agent response: {state['messages'][-1].content[:100]}...")
        
        # Router decision
        decision = should_continue(state)
        
        if decision == "tool":
            print("Routing to tool node...")
            state = call_tool(state)
            print(f"Tool result: {state['messages'][-1].content[:100]}...")
        else:
            print("Routing to end.")
            break
    
    return state

# Run the agent graph
result = run_agent_graph("What is LangGraph?")
print(f"\nFinal response: {result['messages'][-1].content}")

print("\n" + "="*80)
print("Note: For full LangGraph functionality, install: pip install langgraph")
print("This example demonstrates the conceptual patterns.")
print("="*80)
