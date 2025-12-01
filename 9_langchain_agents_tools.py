"""
LangChain Example 7: Agents and Tool Calling (LangChain 1.0+ Compatible)

WHAT ARE AGENTS?
================
Agents are LLMs that can:
1. REASON about which tools to use
2. ACT by calling tools
3. OBSERVE the results
4. REPEAT until the task is complete

LANGCHAIN 1.0+ AGENT PATTERNS:
===============================
 Tool Calling Agents (Recommended for most use cases)
   - Modern, uses native LLM tool calling
   - Best for: GPT-4, Gemini, Claude with function calling

 ReAct Agents (When tool calling isn't available)
   - Uses prompting to guide reasoning
   - Best for: Models without native tool calling

 DEPRECATED: Old agent patterns (ZeroShot, ConversationalAgent)

USE CASES:
==========
- Research assistants (search + summarize)
- Data analysis (calculate + plot + reason)
- Customer support (lookup + action + respond)
- Task automation (multi-step workflows)

WHEN TO USE AGENTS VS LANGGRAPH:
=================================
Use Agents when:
  - Simple tool calling workflows
  - Linear decision making
  - Quick prototypes

Use LangGraph when:
  - Complex state management
  - Cyclic workflows
  - Human-in-the-loop
  - Multi-agent systems
"""

import json
from typing import Any, List

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# ============================================================================
# AGENT EXECUTOR (LangChain 1.0+ Pattern)
# ============================================================================
# This implements the tool-calling agent pattern
# In production, you can use: from langchain.agents import AgentExecutor


class ToolCallingAgent:
    """
    Modern LangChain 1.0+ agent using native tool calling.
    Follows the pattern: Reason → Call Tool → Observe → Repeat
    """

    def __init__(self, llm_with_tools, tools: List[Any], max_iterations: int = 5):
        self.llm = llm_with_tools  # LLM with .bind_tools() already called
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.verbose = True

    def invoke(self, input_dict: dict) -> dict:
        """Execute the agent with tool calling loop."""
        messages: List[BaseMessage] = [HumanMessage(content=input_dict["input"])]
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1

            # Call LLM with current message history
            response = self.llm.invoke(messages)
            messages.append(response)

            if self.verbose:
                content_preview = (response.content or "")[:80]
                print(f"\n [Iteration {iteration}] {content_preview}...")

            # Check if LLM wants to call tools
            if hasattr(response, "tool_calls") and response.tool_calls:
                # Process each tool call
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call.get("args", {})
                    tool_id = tool_call.get("id", f"call_{iteration}")

                    if self.verbose:
                        args_str = json.dumps(tool_args, indent=2)
                        print(f"   Calling: {tool_name}")
                        print(f"     Args: {args_str}")

                    # Execute the tool
                    if tool_name in self.tools:
                        try:
                            result = self.tools[tool_name].invoke(tool_args)
                            if self.verbose:
                                result_preview = str(result)[:100]
                                print(f"   Result: {result_preview}...")

                            # Add tool result to message history
                            tool_message = ToolMessage(
                                content=str(result), tool_call_id=tool_id
                            )
                            messages.append(tool_message)
                        except Exception as e:
                            error_msg = f"Error executing {tool_name}: {e}"
                            print(f"   {error_msg}")
                            messages.append(
                                ToolMessage(content=error_msg, tool_call_id=tool_id)
                            )
                    else:
                        print(f"    Tool '{tool_name}' not found!")
            else:
                # No tool calls - agent has finished reasoning
                if self.verbose:
                    print("   No more tools to call. Task complete.")
                break

        # Return final response
        if messages:
            last_msg = messages[-1]
            # Extract clean text content
            if hasattr(last_msg, "content"):
                if isinstance(last_msg.content, str):
                    final_content = last_msg.content
                elif isinstance(last_msg.content, list):
                    # Handle structured content
                    final_content = " ".join(
                        item.get("text", "")
                        for item in last_msg.content
                        if isinstance(item, dict) and "text" in item
                    )
                else:
                    final_content = str(last_msg.content)
            else:
                final_content = str(last_msg)
        else:
            final_content = "No response"

        return {"output": final_content, "messages": messages}


# ============================================================================
# STEP 1: Define Tools (The @tool decorator is LangChain 1.0+ standard)
# ============================================================================
# Tools are functions that agents can call to perform actions
# The docstring is CRITICAL - LLM uses it to decide when to call the tool


@tool
def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    Use this for any arithmetic calculations.

    Args:
        expression: A math expression like '23 * 7' or '100 / 4'

    Returns:
        The calculated result as a string
    """
    try:
        # In production, use a safer evaluator like numexpr or ast.literal_eval
        result = eval(expression)  # noqa: S307
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@tool
def search_knowledge_base(query: str) -> str:
    """
    Searches a knowledge base for information about LangChain and AI.
    Use this when you need facts about LangChain, agents, or AI concepts.

    Args:
        query: The search query

    Returns:
        Relevant information from the knowledge base
    """
    # Simulated knowledge base
    knowledge = {
        "langchain": "LangChain is a framework for building applications "
        "powered by language models. It provides tools for "
        "chains, agents, memory, and more.",
        "agents": "Agents use LLMs to decide which tools to call and in "
        "what order. They follow a ReAct pattern: Reason, "
        "Act, Observe.",
        "tools": "Tools are functions that agents can call to perform "
        "specific actions like search, calculation, or API calls.",
    }

    # Simple keyword matching
    for key, value in knowledge.items():
        if key in query.lower():
            return value

    return (
        f"No specific information found for '{query}'. Try asking about "
        "LangChain, agents, or tools."
    )


@tool
def get_current_temperature(location: str) -> str:
    """
    Gets the current temperature for a given location.
    Use this when users ask about weather or temperature.

    Args:
        location: City or location name

    Returns:
        Current temperature information
    """
    # Simulated weather data
    temps = {
        "new york": "72°F (22°C)",
        "london": "65°F (18°C)",
        "tokyo": "78°F (26°C)",
        "paris": "68°F (20°C)",
    }

    temp = temps.get(location.lower(), "Unknown")
    if temp == "Unknown":
        return (
            f"Temperature data not available for '{location}'. "
            "Try: New York, London, Tokyo, or Paris."
        )
    return f"Current temperature in {location.title()}: {temp}"


# Collect all tools
tools = [calculate, search_knowledge_base, get_current_temperature]


# ============================================================================
# STEP 2: Create LLM with Tool Binding (LangChain 1.0+ Pattern)
# ============================================================================
# .bind_tools() is the modern way to enable tool calling
# The LLM will receive tool schemas and can decide when to call them

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0).bind_tools(tools)


# ============================================================================
# STEP 3: Create the Agent
# ============================================================================
# In LangChain 1.0+, agents are simpler - just LLM + tools + loop

agent = ToolCallingAgent(llm_with_tools=llm, tools=tools, max_iterations=5)

# ============================================================================
# STEP 4: Run the Agent with Different Queries
# ============================================================================

print("\n" + "=" * 80)
print("AGENTS & TOOL CALLING - LangChain 1.0+")
print("=" * 80)


# Example 1: Simple calculation (single tool call)
print("\n" + "=" * 80)
print("EXAMPLE 1: Single Tool Call (Calculator)")
print("=" * 80)
result = agent.invoke({"input": "What is 127 * 43?"})
print(f"\n Final Answer: {result['output']}\n")


# Example 2: Knowledge base search
print("\n" + "=" * 80)
print("EXAMPLE 2: Knowledge Base Search")
print("=" * 80)
result = agent.invoke({"input": "What are agents in LangChain?"})
print(f"\n Final Answer: {result['output']}\n")


# Example 3: Multi-step reasoning (multiple tool calls)
print("\n" + "=" * 80)
print("EXAMPLE 3: Multi-Step Reasoning (Multiple Tools)")
print("=" * 80)
result = agent.invoke(
    {"input": "Calculate 15 * 8, then tell me what you know about " "LangChain tools"}
)
print(f"\n Final Answer: {result['output']}\n")


# Example 4: Weather query
print("\n" + "=" * 80)
print("EXAMPLE 4: Weather Information")
print("=" * 80)
result = agent.invoke({"input": "What's the temperature in Tokyo?"})
print(f"\n Final Answer: {result['output']}\n")


# Example 5: No tool needed (direct response)
print("\n" + "=" * 80)
print("EXAMPLE 5: Direct Response (No Tools Needed)")
print("=" * 80)
result = agent.invoke({"input": "Say hello in Spanish"})
print(f"\n Final Answer: {result['output']}\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "=" * 80)
print("KEY TAKEAWAYS - Agents in LangChain 1.0+")
print("=" * 80)
print(
    """
 MODERN AGENT PATTERN:
   1. Define tools with @tool decorator
   2. Use .bind_tools() to attach tools to LLM
   3. Implement agent loop: LLM → Tool Call → Tool Execute → Repeat
   4. LLM decides when to stop

 TOOL BEST PRACTICES:
   - Write clear, detailed docstrings (LLM reads these!)
   - Use type hints for arguments
   - Return strings (easier for LLM to parse)
   - Handle errors gracefully

 WHEN TO USE TOOLS:
   - External API calls (weather, search, databases)
   - Calculations and data processing
   - File operations
   - Any action beyond the LLM's training data

 PRODUCTION TIPS:
   - Add retry logic for tool failures
   - Implement rate limiting
   - Log all tool calls for debugging
   - Use async tools for better performance

 FOR COMPLEX WORKFLOWS:
   - Use LangGraph for stateful, multi-step processes
   - See: 8_langchain_langgraph.py for advanced patterns
"""
)

print("=" * 80)
print(" All agent examples completed successfully!")
print("=" * 80)
