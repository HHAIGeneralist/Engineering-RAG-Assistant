from langchain_ollama import OllamaEmbeddings
from src.config import get_settings


def get_embedding_model() -> OllamaEmbeddings:
    settings = get_settings()
    return OllamaEmbeddings(
        model=settings.ollama_embedding_model,
        base_url=settings.ollama_base_url,
        validate_model_on_init=True,
    )
