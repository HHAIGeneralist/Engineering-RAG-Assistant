from langchain_core.documents import Document
from src.chunker import split_documents

def test_chunks_keep_page_metadata():
    doc = Document(page_content="Engineering content. " * 500, metadata={"source_file": "manual.pdf", "page": 7})
    chunks = split_documents([doc])
    assert chunks
    assert all(c.metadata["page"] == 7 for c in chunks)
    assert all(c.metadata.get("chunk_id") for c in chunks)
