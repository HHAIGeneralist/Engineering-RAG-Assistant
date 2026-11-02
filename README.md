# Engineering RAG Assistant

A local Retrieval-Augmented Generation application for querying engineering PDFs with page-level citations. It uses Ollama for an open-weight chat model and embedding model, Qdrant for vector search, Streamlit for the interface, and FastAPI for API access.

**Demonstration**

Live demonstration: Not publicly hosted because the project uses local Ollama models
API documentation: Available locally at http://localhost:8000/docs

**Key Features**
Local open-weight LLM through Ollama
Local embedding generation
Page-aware PDF ingestion
Qdrant vector search
Answers grounded in retrieved passages
Page-level citations
Expandable supporting evidence
FastAPI backend
Streamlit user interface
Docker deployment
No paid LLM API required for local use

**Current Limitations**
Text-based PDFs only; scanned PDFs require OCR.
Tables and complex diagrams may require specialised parsing.
The current release uses dense retrieval without reranking.
Citation presence is validated, but full claim-level citation completeness is still under development.
Public hosting requires a remotely accessible model server or a hosted open-weight inference provider.

## Architecture

PDFs -> PyMuPDF -> cleaning -> chunking -> Ollama embeddings -> Qdrant -> retrieval -> Ollama chat model -> cited answer

## Required software

- Python 3.11 or 3.12
- Git
- Docker Desktop
- Ollama

## 1. Install Ollama models

```powershell
ollama pull qwen2.5:7b
ollama pull qwen3-embedding:0.6b
ollama list
```

If the 7B chat model is too slow, use `qwen2.5:3b` and change `OLLAMA_CHAT_MODEL` in `.env`.

## 2. Create Python environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 3. Configure

```powershell
Copy-Item .env.example .env
```

The defaults use Ollama at `http://localhost:11434` and Qdrant at `http://localhost:6333`.

## 4. Start Qdrant

```powershell
docker compose up -d qdrant
```

Open `http://localhost:6333/dashboard` to inspect the database.

## 5. Add documents

Copy public, text-based PDF manuals into `data/raw/`. Scanned PDFs require OCR before ingestion.

## 6. Ingest

Run from the repository root:

```powershell
python -m scripts.ingest_documents
```

The script recreates the collection to avoid duplicates during development.

## 7. Run Streamlit

```powershell
streamlit run streamlit_app.py
```

Open `http://localhost:8501`.

## 8. Run FastAPI

```powershell
uvicorn api:app --reload
```

Open `http://localhost:8000/docs`.

Example request:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/query -ContentType "application/json" -Body '{"question":"What checks are required before startup?","top_k":6}'
```

## 9. Run tests

```powershell
pytest -v
```

## Full Docker operation

Keep Ollama running on Windows, then run:

```powershell
docker compose up --build -d
```

Ingest inside the app container:

```powershell
docker compose exec app python -m scripts.ingest_documents
```

Open Streamlit at `http://localhost:8501` and the API at `http://localhost:8000/docs`.

## Important constraints

- Use the same embedding model for ingestion and retrieval. If the embedding model changes, recreate the Qdrant collection.
- Citations are accepted only when the model cites a retrieved source ID.
- Verify safety-critical guidance against the original manual.
- Do not upload confidential documents to a public deployment.
- Local Ollama is not reachable from Streamlit Community Cloud. For remote deployment, host Ollama on a secured GPU/CPU server or use another hosted open-weight inference service, then set `OLLAMA_BASE_URL` accordingly.

## Suggested next improvements

- OCR for scanned PDFs
- Hybrid dense/sparse retrieval
- Cross-encoder reranking
- Metadata filters for equipment model and manual version
- Citation completeness evaluation
- Authentication, rate limiting and audit logs
