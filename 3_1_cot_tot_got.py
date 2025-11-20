"""
LangChain Example 3.2: Simple One-Shot Examples of CoT, ToT, and GoT
Demonstrates the three major reasoning patterns with single prompt examples.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# ============================================================================
# PATTERN 1: CHAIN OF THOUGHT (CoT)
# Sequential step-by-step reasoning in a linear path
# ============================================================================

def chain_of_thought_example():
    """
    Chain of Thought: Step-by-step reasoning through a problem
    """
    print("="*80)
    print("PATTERN 1: CHAIN OF THOUGHT (CoT)")
    print("="*80)
    
    cot_prompt = ChatPromptTemplate.from_template(
        """Solve this problem using step-by-step reasoning. Show your work clearly.

Problem: {question}

Instructions:
1. Break down the problem into steps
2. Solve each step sequentially
3. Show your reasoning for each step
4. Provide the final answer

Solution:
"""
    )
    
    cot_chain = cot_prompt | llm | StrOutputParser()
    
    question = "If a store sells apples at $3 per kg and oranges at $4 per kg, and I buy 2.5 kg of apples and 1.5 kg of oranges with a 10% discount on the total, how much do I pay?"
    
    print(f"\n📝 Question: {question}\n")
    print("🔗 Chain of Thought Reasoning:\n")
    
    result = cot_chain.invoke({"question": question})
    print(result)
    print()


# ============================================================================
# PATTERN 2: TREE OF THOUGHT (ToT)
# Explore multiple reasoning paths and compare them
# ============================================================================

def tree_of_thought_example():
    """
    Tree of Thought: Explore multiple reasoning branches simultaneously
    """
    print("="*80)
    print("PATTERN 2: TREE OF THOUGHT (ToT)")
    print("="*80)
    
    tot_prompt = ChatPromptTemplate.from_template(
        """Solve this problem by exploring MULTIPLE different reasoning paths, then compare them.

Problem: {question}

Instructions:
1. Generate 3 DIFFERENT approaches to solve this problem
2. Label them as Path A, Path B, and Path C
3. For each path, show the reasoning and conclusion
4. Evaluate which path is most effective and why
5. Provide the final answer based on the best path

Solution:
"""
    )
    
    tot_chain = tot_prompt | llm | StrOutputParser()
    
    question = "Should a startup prioritize growth or profitability in its first 2 years?"
    
    print(f"\n📝 Question: {question}\n")
    print("🌳 Tree of Thought - Multiple Paths:\n")
    
    result = tot_chain.invoke({"question": question})
    print(result)
    print()


# ============================================================================
# PATTERN 3: GRAPH OF THOUGHT (GoT)
# Build interconnected reasoning with dependencies between concepts
# ============================================================================

def graph_of_thought_example():
    """
    Graph of Thought: Interconnected reasoning with dependencies
    """
    print("="*80)
    print("PATTERN 3: GRAPH OF THOUGHT (GoT)")
    print("="*80)
    
    got_prompt = ChatPromptTemplate.from_template(
        """Solve this problem by building a graph of interconnected reasoning nodes.

Problem: {question}

Instructions:
1. Identify 4-5 key sub-questions or concepts (nodes) needed to solve this problem
2. For each node, identify its dependencies (which other nodes it relies on)
3. Solve the nodes in dependency order (solve dependencies first)
4. Show how insights from one node inform others
5. Synthesize all nodes into a final comprehensive answer

Use this format:
NODE [name]: [description]
DEPENDS ON: [list of nodes or "none"]
SOLUTION: [reasoning and answer for this node]

Final Synthesis: [integrate all nodes]

Solution:
"""
    )
    
    got_chain = got_prompt | llm | StrOutputParser()
    
    question = "How can a city reduce traffic congestion while improving air quality and maintaining economic activity?"
    
    print(f"\n📝 Question: {question}\n")
    print("🕸️  Graph of Thought - Interconnected Reasoning:\n")
    
    result = got_chain.invoke({"question": question})
    print(result)
    print()


# ============================================================================
# BONUS: COMPARISON EXAMPLE
# Show all three patterns on the same problem
# ============================================================================

def comparison_example():
    """
    Compare all three patterns on the same problem
    """
    print("="*80)
    print("BONUS: COMPARING CoT, ToT, and GoT ON THE SAME PROBLEM")
    print("="*80)
    
    problem = "What's the best way to learn a new programming language?"
    
    # CoT prompt
    cot_prompt = ChatPromptTemplate.from_template(
        """Using Chain of Thought (step-by-step reasoning), answer: {question}

Provide a clear, sequential reasoning process.
"""
    )
    
    # ToT prompt
    tot_prompt = ChatPromptTemplate.from_template(
        """Using Tree of Thought (multiple paths), answer: {question}

Generate 3 different approaches and compare them.
"""
    )
    
    # GoT prompt
    got_prompt = ChatPromptTemplate.from_template(
        """Using Graph of Thought (interconnected nodes), answer: {question}

Identify key sub-questions, their dependencies, and synthesize them.
"""
    )
    
    print(f"\n📝 Problem: {problem}\n")
    
    # Execute CoT
    print("-" * 80)
    print("CHAIN OF THOUGHT APPROACH:")
    print("-" * 80)
    cot_result = (cot_prompt | llm | StrOutputParser()).invoke({"question": problem})
    print(cot_result)
    print()
    
    # Execute ToT
    print("-" * 80)
    print("TREE OF THOUGHT APPROACH:")
    print("-" * 80)
    tot_result = (tot_prompt | llm | StrOutputParser()).invoke({"question": problem})
    print(tot_result)
    print()
    
    # Execute GoT
    print("-" * 80)
    print("GRAPH OF THOUGHT APPROACH:")
    print("-" * 80)
    got_result = (got_prompt | llm | StrOutputParser()).invoke({"question": problem})
    print(got_result)
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("SIMPLE ONE-SHOT EXAMPLES: CoT, ToT, and GoT")
    print("="*80 + "\n")
    
    # Run individual examples
    chain_of_thought_example()
    print("\n")
    
    tree_of_thought_example()
    print("\n")
    
    graph_of_thought_example()
    print("\n")
    
    # Run comparison
    # comparison_example()
    
    print("="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80 + "\n")
