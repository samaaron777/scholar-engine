import chromadb

from sentence_transformers import SentenceTransformer


# Embedding Model

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Chroma Client

client = chromadb.Client()


# Create Collection

collection = client.get_or_create_collection(
    name="research_memory"
)


# Add Documents

def add_to_vector_store(text, metadata=None):

    embedding = embedding_model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata or {}],
        ids=[str(hash(text))]
    )


# Search Similar Documents

def search_vector_store(query, top_k=3):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results