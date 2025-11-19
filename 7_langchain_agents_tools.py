"""
LangChain Example 7: Agents and Tool Calling
Demonstrates ReAct pattern: Reason -> Act -> Observe -> Repeat.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

# Simplified agent executor (since langchain.agents may not be available)
class SimpleAgentExecutor:
    def __init__(self, llm, tools, prompt, max_iterations=5):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.prompt = prompt
        self.max_iterations = max_iterations
        self.verbose = True
    
    def invoke(self, input_dict):
        messages = [HumanMessage(content=input_dict["input"])]
        
        for i in range(self.max_iterations):
            # Format prompt with messages
            formatted = self.prompt.format_messages(
                input=input_dict["input"],
                agent_scratchpad=messages[1:] if len(messages) > 1 else []
            )
            
            # Call LLM
            response = self.llm.invoke(formatted)
            messages.append(response)
            
            if self.verbose:
                print(f"\n[Iteration {i+1}] LLM Response: {response.content[:100]}...")
            
            # Check for tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_call = response.tool_calls[0]
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                
                if self.verbose:
                    print(f"[Tool Call] {tool_name}({tool_args})")
                
                # Execute tool
                tool_func = self.tools.get(tool_name)
                if tool_func:
                    result = tool_func.invoke(tool_args)
                    tool_message = ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call.get("id", "1")
                    )
                    messages.append(tool_message)
                else:
                    break
            else:
                # No tool call, we're done
                break
        
        return {"output": messages[-1].content if messages else "No response"}

# 1. Define tools
@tool
def search_web(query: str) -> str:
    """
    Searches the web for relevant information on a given query.
    Use this for up-to-date information, news, or general facts.
    """
    print(f"--- Calling Search Tool with query: {query} ---")
    return f"Search results for '{query}': LangChain is a framework for building LLM applications."

@tool
def calculate(expression: str) -> str:
    """
    Evaluates a simple math expression (e.g., '23 * 7').
    Use this for arithmetic.
    """
    print(f"--- Calling Calculate Tool with expression: {expression} ---")
    try:
        # In production, use a safer evaluator like numexpr
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [search_web, calculate]

# 2. Bind tools to the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0).bind_tools(tools)

# 3. Create the Agent Prompt
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools if necessary."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # Where tool outputs go
])

# 4. Create the Executor (simplified version)
executor = SimpleAgentExecutor(llm, tools, agent_prompt)

print("="*80)
print("Agents and Tool Calling")
print("="*80)

print("\n--- Query 1: Math ---")
result = executor.invoke({"input": "What is 23 * 7?"})
print(f"Result: {result['output']}")

print("\n--- Query 2: Search ---")
result = executor.invoke({"input": "What is LangChain?"})
print(f"Result: {result['output']}")

print("\n--- Query 3: No Tool Needed ---")
result = executor.invoke({"input": "Hello, how are you?"})
print(f"Result: {result['output']}")

