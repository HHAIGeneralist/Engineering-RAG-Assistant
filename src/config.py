from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "Engineering RAG Assistant"
    data_dir: Path = PROJECT_ROOT / "data" / "raw"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "engineering_documents"
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "qwen2.5:7b"
    ollama_embedding_model: str = "qwen3-embedding:0.6b"
    chunk_size: int = Field(default=3000, ge=500, le=10000)
    chunk_overlap: int = Field(default=400, ge=0, le=2000)
    retrieval_top_k: int = Field(default=6, ge=1, le=20)
    max_upload_mb: int = Field(default=25, ge=1, le=200)

@lru_cache
def get_settings() -> Settings:
    return Settings()
