from langchain_core.documents import Document
from src.config import get_settings
from src.vector_store import get_vector_store


def retrieve_documents(question: str, top_k: int | None = None) -> list[Document]:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    s = get_settings()
    return get_vector_store().similarity_search(question, k=top_k or s.retrieval_top_k)
