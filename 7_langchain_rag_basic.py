"""
LangChain Example 5: Basic RAG Pipeline (LangChain 1.0+ Compatible)

WHAT IS RAG (Retrieval-Augmented Generation)?
==============================================
RAG is a technique that enhances LLM responses by combining:
1. **Retrieval**: Finding relevant information from a knowledge base
2. **Augmentation**: Adding retrieved context to the user's query
3. **Generation**: LLM generates an answer based on the context

WHY USE RAG?
============
-  Reduces hallucinations by grounding answers in real data
-  Enables LLMs to access up-to-date or domain-specific information
-  More cost-effective than fine-tuning for knowledge updates
-  Provides source attribution and transparency

HOW THIS EXAMPLE ACHIEVES RAG:
==============================
Stage 1: INDEXING (Lines 61-72)
    - Create knowledge base (sample documents about LangChain)
    - Convert text to embeddings (numerical representations)
    - Store embeddings in vector store for semantic search

Stage 2: RETRIEVAL (Lines 80, 98-100)
    - User asks a question
    - Convert question to embedding
    - Find most similar documents using cosine similarity
    - Return top-k relevant chunks

Stage 3: AUGMENTATION & GENERATION (Lines 83-108)
    - Inject retrieved context into prompt template
    - LLM receives: context + user question
    - LLM generates answer based ONLY on provided context

LANGCHAIN 1.0 COMPATIBILITY:
============================
 Uses langchain_core imports (modern architecture)
 Uses LCEL (LangChain Expression Language) with | operator
 Uses Runnable interface (.invoke() method)
 Type-safe with proper annotations
 Compatible with langchain-google-genai>=2.0.0
"""

from typing import Any

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

load_dotenv()


# ============================================================================
# VECTOR STORE IMPLEMENTATION (For RAG Stage 1: Indexing)
# ============================================================================
# Simple in-memory vector store for demonstration
# In production, use: Chroma, Pinecone, FAISS, Weaviate, etc.


class SimpleVectorStore:
    """
    Stores text chunks and their embeddings for semantic search.
    This is the "knowledge base" that RAG retrieves from.
    """

    def __init__(self, texts, embeddings_model):
        self.texts = texts
        self.embeddings_model = embeddings_model
        # INDEXING: Convert all texts to embeddings (vectors)
        # This happens once during setup, not per query
        print("Generating embeddings...")
        self.embeddings = embeddings_model.embed_documents(texts)

    def as_retriever(self, k=2):
        """Returns a retriever that implements the Runnable interface."""
        return SimpleRetriever(self, k)


class SimpleRetriever:
    """
    Retrieves most relevant documents for a query using semantic search.
    Implements .invoke() for LangChain 1.0 Runnable compatibility.
    """

    def __init__(self, store, k):
        self.store = store
        self.k = k  # Number of documents to retrieve

    def invoke(self, query):
        """
        RETRIEVAL STAGE: Find most similar documents to the query.
        1. Convert query to embedding
        2. Calculate similarity with all stored embeddings
        3. Return top-k most similar documents
        """
        # Convert user's question to same embedding space
        query_embedding = self.store.embeddings_model.embed_query(query)

        # Calculate cosine similarities (measures angle between vectors)
        def cosine_similarity(vec1, vec2):
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            return dot_product / (norm1 * norm2) if norm1 * norm2 > 0 else 0

        # Compare query embedding with all document embeddings
        similarities = [
            cosine_similarity(query_embedding, emb) for emb in self.store.embeddings
        ]

        # Sort by similarity score (highest first) and get top-k
        indexed_sims = list(enumerate(similarities))
        indexed_sims.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in indexed_sims[: self.k]]

        # Return as LangChain Document objects
        return [Document(page_content=self.store.texts[i]) for i in top_indices]


# ============================================================================
# STAGE 1: INDEXING (Done once - build the knowledge base)
# ============================================================================
# UNPUBLISHED MOVIE SCREENPLAY (Unknown to the LLM)
# "The Last Cipher" - Written by Director Sofia Ramirez (2023)
# This demonstrates RAG's power: LLM can answer questions about content
# it was NEVER trained on, by retrieving relevant context.

texts = [
    """The Last Cipher is a sci-fi thriller directed by Sofia Ramirez.
    The story follows Dr. Elena Kovacs, a cryptographer who discovers
    an ancient alien message hidden in Earth's magnetic field. The
    message warns of an invasion scheduled for 2157, exactly 100 years
    after humanity first detected it.""",
    """The protagonist, Dr. Elena Kovacs, is a brilliant but reclusive
    cryptographer working at CERN. Her mentor, Professor Marcus Chen,
    was killed under mysterious circumstances after claiming he decoded
    part of the alien message. Elena partners with ex-military pilot
    Captain James Rivera to uncover the truth.""",
    """The antagonist is Director Sarah Walsh of the Global Security
    Council, who secretly knows about the invasion. Walsh has been
    working with a faction of aliens called the Architects, believing
    they will spare humanity if she helps them sabotage Earth's defense
    preparations. Her assistant, Dr. Thomas Park, is an alien hybrid.""",
    """The plot twist occurs in Act 3 when Elena discovers the 'invasion'
    message is actually a test. The Architects want to see if humanity
    can unite and decode their message. By working together across
    nations, Elena and Rivera prove humanity's worthiness, turning
    potential enemies into allies.""",
    """The climax takes place at the Aurora Research Station in Norway
    where Elena must choose: destroy the decoding device and hide from
    the Architects, or complete the message and face first contact.
    Rivera sacrifices himself to buy Elena time, getting shot by Walsh's
    security forces.""",
    """The resolution sees Elena completing the cipher, which unlocks
    advanced technology blueprints for clean energy and space travel.
    Walsh is arrested for treason. The film ends with Elena receiving
    a Nobel Peace Prize, and humanity's first FTL ship, named 'The
    Rivera,' launching toward the Architect homeworld.""",
]

# Convert texts to embeddings and store them
# GoogleGenerativeAIEmbeddings: Converts text → vectors (numbers)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = SimpleVectorStore(texts, embeddings_model)

print("=" * 80)
print("RAG DEMONSTRATION: Unpublished Movie Screenplay")
print("=" * 80)
print("\n Knowledge Base: 'The Last Cipher' by Director Sofia Ramirez")
print("This unpublished screenplay was NEVER seen during LLM training")
print("RAG will retrieve relevant context to answer questions accurately\n")

# ============================================================================
# STAGE 2 & 3: RETRIEVAL + GENERATION (Done per user query)
# ============================================================================

# Create retriever that will find relevant documents
retriever = vector_store.as_retriever(k=2)  # Retrieve top 2 most relevant

# Define prompt template for AUGMENTATION
# This injects retrieved context into the LLM's prompt
rag_prompt = ChatPromptTemplate.from_template(
    """Answer the user's question based only on the following context:

<context>
{context}
</context>

Question: {question}

Answer:"""
)


# Helper function to retrieve and format documents
def retrieve_docs(query: str) -> str:
    """
    RETRIEVAL STAGE: Get relevant docs and format as context string.
    This is called automatically when the chain runs.
    """
    docs = retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs)


# ============================================================================
# BUILD RAG CHAIN using LCEL (LangChain Expression Language)
# ============================================================================
# Flow: Query → Retrieve Context → Augment Prompt → Generate Answer
rag_chain: Any = (
    # Parallel execution: retrieve context AND pass through question
    {
        "context": RunnableLambda(retrieve_docs),  # Retrieves docs
        "question": RunnablePassthrough(),  # Passes query as-is
    }
    | rag_prompt  # Inject context + question into template
    | ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)  # Generate
    | StrOutputParser()  # Extract string from AI message
)
# LangChain 1.0: The | operator chains Runnables together
# Each component's output becomes the next component's input


# ============================================================================
# EXECUTE RAG PIPELINE
# ============================================================================
# When you call .invoke(), here's what happens:
# 1. RETRIEVAL: retrieve_docs() finds similar documents
# 2. AUGMENTATION: Context is injected into the prompt
# 3. GENERATION: LLM answers based on the context

print("\n" + "=" * 80)
print("Testing RAG: LLM knows NOTHING about this unpublished movie")
print("Without RAG, it would hallucinate or say 'I don't know'")
print("=" * 80)

print("\n Query: What is 'The Last Cipher' about?")
result = rag_chain.invoke("What is 'The Last Cipher' about?")
print(f" Answer: {result}")
print(" RAG retrieved the movie plot from the screenplay\n")

print(" Query: Who are the main characters and what are their roles?")
result = rag_chain.invoke("Who are the main characters and what are their roles?")
print(f" Answer: {result}")
print(" RAG found character information from multiple chunks\n")

print(" Query: What is the major plot twist in the movie?")
result = rag_chain.invoke("What is the major plot twist in the movie?")
print(f" Answer: {result}")
print(" RAG retrieved the Act 3 twist about the test\n")

print(" Query: How does the movie end?")
result = rag_chain.invoke("How does the movie end?")
print(f" Answer: {result}")
print(" RAG found the resolution and ending details\n")

print("=" * 80)
print(" RAG SUCCESS: All answers from unpublished screenplay")
print("Without RAG, LLM couldn't answer ANY of these questions!")
print("=" * 80)
