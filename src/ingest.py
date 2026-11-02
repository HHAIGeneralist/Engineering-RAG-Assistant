from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models
from src.chunker import split_documents
from src.config import get_settings
from src.embeddings import get_embedding_model
from src.pdf_loader import load_pdf_pages
from src.text_cleaner import clean_documents
from src.vector_store import get_qdrant_client


def build_chunks(pdf_paths: list[Path]):
    all_chunks = []
    for pdf_path in pdf_paths:
        pages = clean_documents(load_pdf_pages(pdf_path))
        chunks = split_documents(pages)
        print(f"{pdf_path.name}: {len(pages)} text pages, {len(chunks)} chunks")
        all_chunks.extend(chunks)
    return all_chunks


def ingest_pdfs(pdf_paths: list[Path], recreate: bool = True) -> int:
    if not pdf_paths:
        raise ValueError("No PDF files supplied.")
    chunks = build_chunks(pdf_paths)
    if not chunks:
        raise RuntimeError("No text chunks were extracted. The PDFs may require OCR.")
    s = get_settings()
    client = get_qdrant_client()
    if recreate and client.collection_exists(s.qdrant_collection):
        client.delete_collection(s.qdrant_collection)
    embeddings = get_embedding_model()
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=s.qdrant_url,
        api_key=s.qdrant_api_key or None,
        collection_name=s.qdrant_collection,
        distance=models.Distance.COSINE,
    )
    return len(chunks)
