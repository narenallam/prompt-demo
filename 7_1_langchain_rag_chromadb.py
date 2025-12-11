"""
LangChain Example 5.1: RAG with ChromaDB Vector Store

WHAT'S DIFFERENT FROM 7_langchain_rag_basic.py?
===============================================
- Uses ChromaDB instead of custom SimpleVectorStore
- Persistent storage (data saved to disk)
- Production-ready vector database
- Better performance for larger datasets
- Built-in metadata filtering and advanced queries

CHROMADB FEATURES:
==================
- Open-source vector database
- Persistent storage (saves embeddings to disk)
- Fast similarity search
- Metadata filtering
- Multiple distance metrics (L2, cosine, IP)
- Works with any embedding model

INSTALLATION:
=============
pip install chromadb langchain-chroma

This example uses the same unpublished movie screenplay to demonstrate
RAG with a production-grade vector store.
"""

from dotenv import load_dotenv
from langchain_chroma import Chroma
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
# STAGE 1: INDEXING WITH CHROMADB
# ============================================================================

print("=" * 80)
print("RAG WITH CHROMADB: Unpublished Movie Screenplay")
print("=" * 80)
print("\nKnowledge Base: 'The Last Cipher' by Director Sofia Ramirez")
print("Using ChromaDB for persistent vector storage\n")

# UNPUBLISHED MOVIE SCREENPLAY - Same as in 7_langchain_rag_basic.py
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

# Create Document objects with metadata (ChromaDB supports rich metadata)
documents = [
    Document(
        page_content=text,
        metadata={
            "source": "The Last Cipher Screenplay",
            "author": "Sofia Ramirez",
            "year": 2023,
            "chunk_id": i,
        },
    )
    for i, text in enumerate(texts)
]

# Initialize embeddings model
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

print("Creating ChromaDB vector store...")
print("Note: This will create a ./chroma_db directory for persistent storage")

# Create ChromaDB vector store
# persist_directory: Where to save the database (persistent storage)
# collection_name: Name for this collection of documents
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings_model,
    collection_name="last_cipher_screenplay",
    persist_directory="./chroma_db",
)

print("✓ Documents indexed in ChromaDB\n")

# ============================================================================
# STAGE 2 & 3: RETRIEVAL + GENERATION
# ============================================================================

# Create retriever from ChromaDB
# k=2: Return top 2 most similar documents
# search_type="similarity": Use cosine similarity (default)
# Other options: "mmr" (Maximal Marginal Relevance) for diversity
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)

# Define RAG prompt template
rag_prompt = ChatPromptTemplate.from_template(
    """Answer the user's question based only on the following context:

<context>
{context}
</context>

Question: {question}

Answer:"""
)


# Helper function to format retrieved documents
def format_docs(docs: list[Document]) -> str:
    """Format retrieved documents as context string."""
    return "\n\n".join(doc.page_content for doc in docs)


# ============================================================================
# BUILD RAG CHAIN WITH CHROMADB
# ============================================================================

rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    }
    | rag_prompt
    | ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    | StrOutputParser()
)

# ============================================================================
# EXECUTE RAG PIPELINE WITH CHROMADB
# ============================================================================

print("=" * 80)
print("Testing RAG with ChromaDB Vector Store")
print("=" * 80)

queries = [
    "What is 'The Last Cipher' about?",
    "Who are the main characters and what are their roles?",
    "What is the major plot twist in the movie?",
    "How does the movie end?",
]

for query in queries:
    print(f"\n🔍 Query: {query}")
    result = rag_chain.invoke(query)
    print(f"💡 Answer: {result}")

    # Optional: Show which documents were retrieved
    retrieved_docs = retriever.invoke(query)
    print(f"📄 Retrieved {len(retrieved_docs)} documents (chunks {', '.join(str(doc.metadata['chunk_id']) for doc in retrieved_docs)})")

print("\n" + "=" * 80)
print("RAG SUCCESS with ChromaDB!")
print("=" * 80)
print("\nChromaDB Advantages:")
print("✓ Persistent storage (data saved to ./chroma_db)")
print("✓ Fast similarity search with optimized indexing")
print("✓ Metadata filtering (can filter by author, year, etc.)")
print("✓ Production-ready and scalable")
print("✓ Easy to add/update/delete documents")
print("\nNext Steps:")
print("- Try metadata filtering: retriever with filter={'author': 'Sofia Ramirez'}")
print("- Experiment with MMR search for diverse results")
print("- Add more documents and see performance at scale")
print("=" * 80)

# ============================================================================
# BONUS: CHROMADB ADVANCED FEATURES
# ============================================================================

print("\n" + "=" * 80)
print("BONUS: ChromaDB Advanced Features")
print("=" * 80)

# 1. Direct similarity search with scores
print("\n1. Similarity search with relevance scores:")
query = "Who is the antagonist?"
docs_with_scores = vector_store.similarity_search_with_score(query, k=2)
for doc, score in docs_with_scores:
    print(f"   Score: {score:.4f}")
    print(f"   Content: {doc.page_content[:100]}...")
    print()

# 2. Metadata filtering
print("2. Metadata filtering (documents from 2023):")
filtered_retriever = vector_store.as_retriever(
    search_kwargs={"k": 2, "filter": {"year": 2023}}
)
filtered_docs = filtered_retriever.invoke("Tell me about the characters")
print(f"   Retrieved {len(filtered_docs)} documents with year=2023 filter")

# 3. MMR (Maximal Marginal Relevance) search for diversity
print("\n3. MMR search (diverse results, not just most similar):")
mmr_retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2, "fetch_k": 4},  # fetch_k: candidates before diversity
)
mmr_docs = mmr_retriever.invoke("Tell me about the movie")
print(f"   Retrieved {len(mmr_docs)} diverse documents")

print("\n" + "=" * 80)
print("ChromaDB Demo Complete!")
print("Database persisted at: ./chroma_db")
print("Run this script again - it will load from disk instantly!")
print("=" * 80)
