from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from qdrant_client.http.exceptions import UnexpectedResponse
from src.config import get_settings
from src.rag_pipeline import answer_question
from src.vector_store import get_qdrant_client

settings = get_settings()
app = FastAPI(title=settings.app_name + " API", version="1.0.0")

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=6, ge=1, le=20)

class Citation(BaseModel):
    source_id: str
    source_file: str | None
    page: int | None
    chunk_id: str | None
    passage: str

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]

@app.get("/health")
def health() -> dict:
    try:
        get_qdrant_client().get_collections()
        return {"status": "healthy", "qdrant": "connected"}
    except Exception as exc:
        return {"status": "degraded", "qdrant": "unavailable", "detail": str(exc)}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> dict:
    try:
        return answer_question(request.question, request.top_k)
    except (UnexpectedResponse, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query failed: {exc}") from exc
