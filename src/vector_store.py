from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from src.config import get_settings
from src.embeddings import get_embedding_model


def get_qdrant_client() -> QdrantClient:
    s = get_settings()
    return QdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key or None)


def get_vector_store() -> QdrantVectorStore:
    s = get_settings()
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=s.qdrant_collection,
        embedding=get_embedding_model(),
    )
