import hashlib
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import get_settings


def _chunk_id(document: Document) -> str:
    raw = f"{document.metadata.get('source_file')}|{document.metadata.get('page')}|{document.page_content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def split_documents(documents: list[Document]) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index
        chunk.metadata["chunk_id"] = _chunk_id(chunk)
    return chunks
