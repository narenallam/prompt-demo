"""
LangChain Example 3.1: Tree of Thought (ToT) and Graph of Thought (GoT) with Self-Reflection
Demonstrates advanced reasoning patterns:
1. Tree of Thought: Exploring multiple reasoning paths in parallel
2. Graph of Thought: Building interconnected reasoning chains
3. Self-Reflection: Critique and revision of outputs
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# ============================================================================
# PATTERN 1: TREE OF THOUGHT (ToT)
# Generate multiple reasoning paths and select the best one
# ============================================================================


def tree_of_thought_pattern():
    """
    Tree of Thought Pattern:
    1. Generate multiple independent reasoning paths
    2. Evaluate each path
    3. Select and refine the best path
    """
    print("=" * 80)
    print("PATTERN 1: TREE OF THOUGHT (ToT)")
    print("=" * 80)

    # Step 1: Generate multiple thought branches
    branch_prompt = ChatPromptTemplate.from_template(
        """You are solving the following problem. Generate ONE unique reasoning approach.
        
Problem: {question}

Approach #{branch_num}:
Provide a distinct reasoning path to solve this problem. Be creative and thorough.
"""
    )

    # Step 2: Evaluate each branch
    evaluate_prompt = ChatPromptTemplate.from_template(
        """Evaluate the following reasoning approach on a scale of 1-10 based on:
1. Logical soundness
2. Completeness
3. Clarity

Reasoning Approach:
{branch}

Provide your evaluation in this format:
Score: [1-10]
Justification: [brief explanation]
"""
    )

    # Step 3: Synthesize the best approach
    synthesize_prompt = ChatPromptTemplate.from_template(
        """Given the following evaluated reasoning paths, synthesize the BEST final answer.

Original Question: {question}

Reasoning Paths and Evaluations:
{all_branches}

Final Answer:
Provide a clear, comprehensive solution that incorporates the strongest aspects of the evaluated paths.
"""
    )

    # Create chains
    branch_chain = branch_prompt | llm | StrOutputParser()
    evaluate_chain = evaluate_prompt | llm | StrOutputParser()
    synthesize_chain = synthesize_prompt | llm | StrOutputParser()

    # Execute ToT pattern
    question = "How can we reduce carbon emissions in urban areas effectively?"

    # Generate multiple branches
    print(f"\n Question: {question}\n")
    print(" Generating multiple reasoning paths...\n")

    branches = []
    evaluations = []

    for i in range(3):
        print(f"Branch {i + 1}:")
        branch = branch_chain.invoke({"question": question, "branch_num": i + 1})
        print(f"{branch}\n")
        branches.append(branch)

        eval_result = evaluate_chain.invoke({"branch": branch})
        print(f"Evaluation: {eval_result}\n")
        evaluations.append(eval_result)

    # Synthesize final answer
    all_branches_text = "\n\n".join(
        [
            f"Path {i + 1}:\n{branch}\n\nEvaluation:\n{eval}"
            for i, (branch, eval) in enumerate(zip(branches, evaluations))
        ]
    )

    print(" Synthesizing final answer...\n")
    final_answer = synthesize_chain.invoke(
        {"question": question, "all_branches": all_branches_text}
    )

    print(f" Final Synthesized Answer:\n{final_answer}\n")


# ============================================================================
# PATTERN 2: GRAPH OF THOUGHT (GoT)
# Build interconnected reasoning chains with dependencies
# ============================================================================


def graph_of_thought_pattern():
    """
    Graph of Thought Pattern:
    1. Break problem into sub-problems (nodes)
    2. Solve sub-problems with awareness of dependencies
    3. Integrate all solutions into a coherent answer
    """
    print("=" * 80)
    print("PATTERN 2: GRAPH OF THOUGHT (GoT)")
    print("=" * 80)

    # Step 1: Decompose into sub-problems
    decompose_prompt = ChatPromptTemplate.from_template(
        """Break down the following complex problem into 3-4 interconnected sub-problems.
For each sub-problem, identify which other sub-problems it depends on.

Problem: {question}

Format your response as:
Sub-problem 1: [description]
Dependencies: [list dependencies or "none"]

Sub-problem 2: [description]
Dependencies: [list dependencies or "none"]

(continue for all sub-problems)
"""
    )

    # Step 2: Solve each sub-problem with context
    solve_subproblem_prompt = ChatPromptTemplate.from_template(
        """Solve the following sub-problem, considering the provided context from related sub-problems.

Main Problem: {main_question}

Current Sub-problem: {subproblem}

Context from Dependencies:
{dependency_context}

Solution:
Provide a thorough solution to this sub-problem.
"""
    )

    # Step 3: Integrate all solutions
    integrate_prompt = ChatPromptTemplate.from_template(
        """Integrate the following sub-problem solutions into a comprehensive final answer.

Original Problem: {question}

Sub-problem Solutions:
{all_solutions}

Integrated Final Answer:
Provide a coherent, complete answer that synthesizes all sub-solutions.
"""
    )

    # Create chains
    decompose_chain = decompose_prompt | llm | StrOutputParser()
    solve_chain = solve_subproblem_prompt | llm | StrOutputParser()
    integrate_chain = integrate_prompt | llm | StrOutputParser()

    # Execute GoT pattern
    question = "Design a sustainable smart city transportation system for 2030"

    print(f"\n Question: {question}\n")
    print(" Decomposing into sub-problems...\n")

    decomposition = decompose_chain.invoke({"question": question})
    print(f"{decomposition}\n")

    print(" Solving sub-problems with dependencies...\n")

    # Simplified: solve sub-problems sequentially, building context
    subproblems = [
        "Infrastructure requirements and energy sources",
        "Traffic management and AI optimization systems",
        "User experience and accessibility features",
    ]

    solutions = []
    context = ""

    for i, subproblem in enumerate(subproblems):
        print(f"Solving Sub-problem {i + 1}: {subproblem}")
        solution = solve_chain.invoke(
            {
                "main_question": question,
                "subproblem": subproblem,
                "dependency_context": context if context else "No prior context",
            }
        )
        print(f"{solution}\n")
        solutions.append(solution)
        context += f"\n\nSolution to '{subproblem}':\n{solution}"

    # Integrate solutions
    print(" Integrating all solutions...\n")
    all_solutions_text = "\n\n".join(
        [
            f"Sub-problem {i + 1}: {sub}\nSolution: {sol}"
            for i, (sub, sol) in enumerate(zip(subproblems, solutions))
        ]
    )

    final_answer = integrate_chain.invoke(
        {"question": question, "all_solutions": all_solutions_text}
    )

    print(f" Integrated Final Answer:\n{final_answer}\n")


# ============================================================================
# PATTERN 3: ToT/GoT WITH SELF-REFLECTION
# Combine ToT or GoT with iterative self-critique and refinement
# ============================================================================


def tot_with_reflection():
    """
    ToT with Self-Reflection:
    1. Generate multiple reasoning paths (ToT)
    2. Select the best path
    3. Apply self-reflection (critique and revise)
    """
    print("=" * 80)
    print("PATTERN 3: TREE OF THOUGHT WITH SELF-REFLECTION")
    print("=" * 80)

    # Generate multiple approaches
    approach_prompt = ChatPromptTemplate.from_template(
        """Generate a reasoning approach to solve this problem.

Problem: {question}
Approach Style: {style}

Provide a detailed reasoning path:
"""
    )

    # Select best approach
    select_prompt = ChatPromptTemplate.from_template(
        """Compare these reasoning approaches and select the best one.

Problem: {question}

Approach 1 (Analytical):
{approach1}

Approach 2 (Creative):
{approach2}

Approach 3 (Practical):
{approach3}

Select the most promising approach and explain why. Then provide an initial solution using that approach.

Response format:
Selected Approach: [1, 2, or 3]
Reasoning: [why this approach is best]
Initial Solution:
[your solution]
"""
    )

    # Critique the solution
    critique_prompt = ChatPromptTemplate.from_template(
        """Critique the following solution based on:
1. Correctness and logical soundness
2. Completeness - are there gaps?
3. Clarity and structure
4. Practical applicability

Original Question: {question}
Solution: {solution}

Provide specific, actionable critique:
"""
    )

    # Revise based on critique
    revise_prompt = ChatPromptTemplate.from_template(
        """Revise the solution based on the critique provided.

Original Question: {question}
Original Solution: {solution}
Critique: {critique}

Revised Solution:
Address all points raised in the critique and provide an improved answer.
"""
    )

    # Create chains
    approach_chain = approach_prompt | llm | StrOutputParser()
    select_chain = select_prompt | llm | StrOutputParser()
    critique_chain = critique_prompt | llm | StrOutputParser()
    revise_chain = revise_prompt | llm | StrOutputParser()

    # Execute pattern
    question = "How can small businesses leverage AI without large budgets?"

    print(f"\n Question: {question}\n")
    print(" Generating diverse reasoning approaches...\n")

    # Generate 3 different styles of approaches
    approach1 = approach_chain.invoke(
        {"question": question, "style": "analytical and data-driven"}
    )
    print(f"Analytical Approach:\n{approach1}\n")

    approach2 = approach_chain.invoke(
        {"question": question, "style": "creative and innovative"}
    )
    print(f"Creative Approach:\n{approach2}\n")

    approach3 = approach_chain.invoke(
        {"question": question, "style": "practical and implementation-focused"}
    )
    print(f"Practical Approach:\n{approach3}\n")

    # Select and generate initial solution
    print(" Selecting best approach and generating solution...\n")
    initial_solution = select_chain.invoke(
        {
            "question": question,
            "approach1": approach1,
            "approach2": approach2,
            "approach3": approach3,
        }
    )
    print(f"Initial Solution:\n{initial_solution}\n")

    # Critique
    print(" Applying self-critique...\n")
    critique = critique_chain.invoke(
        {"question": question, "solution": initial_solution}
    )
    print(f"Critique:\n{critique}\n")

    # Revise
    print(" Revising based on critique...\n")
    final_solution = revise_chain.invoke(
        {"question": question, "solution": initial_solution, "critique": critique}
    )
    print(f" Final Revised Solution:\n{final_solution}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ADVANCED REASONING PATTERNS WITH LANGCHAIN")
    print("=" * 80 + "\n")

    # Run all patterns
    tree_of_thought_pattern()
    print("\n" + "-" * 80 + "\n")

    graph_of_thought_pattern()
    print("\n" + "-" * 80 + "\n")

    tot_with_reflection()

    print("\n" + "=" * 80)
    print("ALL PATTERNS COMPLETED")
    print("=" * 80 + "\n")
