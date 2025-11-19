"""
LangChain Example 5: Basic RAG Pipeline
Demonstrates Retrieval-Augmented Generation: Retrieve -> Augment -> Generate.
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.documents import Document

# Simple in-memory vector store for demonstration
class SimpleVectorStore:
    def __init__(self, texts, embeddings_model):
        self.texts = texts
        self.embeddings_model = embeddings_model
        # Generate embeddings for all texts
        print("Generating embeddings...")
        self.embeddings = embeddings_model.embed_documents(texts)
    
    def as_retriever(self, k=2):
        return SimpleRetriever(self, k)

class SimpleRetriever:
    def __init__(self, store, k):
        self.store = store
        self.k = k
    
    def invoke(self, query):
        # Simple similarity search (cosine similarity)
        query_embedding = self.store.embeddings_model.embed_query(query)
        
        # Calculate cosine similarities (without numpy)
        def cosine_similarity(vec1, vec2):
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            return dot_product / (norm1 * norm2) if norm1 * norm2 > 0 else 0
        
        similarities = [cosine_similarity(query_embedding, emb) for emb in self.store.embeddings]
        
        # Get top k
        indexed_sims = list(enumerate(similarities))
        indexed_sims.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in indexed_sims[:self.k]]
        return [Document(page_content=self.store.texts[i]) for i in top_indices]

# --- 1. INDEXING (Done once) ---
# Create sample documents
texts = [
    "LangChain connects LLMs with external data sources.",
    "Embeddings are numerical representations of meaning.",
    "LangGraph is used for building stateful, cyclic applications.",
    "RAG combines retrieval with generation for accurate answers.",
    "Vector stores enable semantic search over documents.",
]

# Embed and store
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = SimpleVectorStore(texts, embeddings_model)

print("="*80)
print("Basic RAG Pipeline")
print("="*80)

# --- 2. RETRIEVAL & GENERATION (Done per query) ---
# Create retriever
retriever = vector_store.as_retriever(k=2)  # Retrieve top 2 chunks

# Define RAG prompt
rag_prompt = ChatPromptTemplate.from_template(
    """Answer the user's question based only on the following context:

<context>
{context}
</context>

Question: {question}

Answer:"""
)

# Create RAG chain
# Wrap retriever in RunnableLambda to make it compatible with LCEL
def retrieve_docs(query: str):
    docs = retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {
        "context": RunnableLambda(retrieve_docs),
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    | StrOutputParser()
)

# Invoke the chain
print("\nQuery: What is LangGraph?")
result = rag_chain.invoke("What is LangGraph?")
print(f"Answer: {result}")

print("\nQuery: How does RAG work?")
result = rag_chain.invoke("How does RAG work?")
print(f"Answer: {result}")
