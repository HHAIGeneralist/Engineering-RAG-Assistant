import re
from langchain_core.documents import Document


def format_sources(documents: list[Document]) -> tuple[str, dict[str, Document]]:
    blocks, source_map = [], {}
    for i, document in enumerate(documents, 1):
        source_id = f"S{i}"
        source_map[source_id] = document
        m = document.metadata
        blocks.append(
            f"[{source_id}]\nDocument: {m.get('source_file', 'Unknown')}\n"
            f"Page: {m.get('page', 'Unknown')}\nChunk ID: {m.get('chunk_id', 'Unknown')}\n"
            f"Text:\n{document.page_content}"
        )
    return "\n\n".join(blocks), source_map


def cited_sources(answer: str, source_map: dict[str, Document]) -> list[dict]:
    ids = list(dict.fromkeys(re.findall(r"\[(S\d+)\]", answer)))
    citations = []
    for source_id in ids:
        document = source_map.get(source_id)
        if document is None:
            continue
        m = document.metadata
        citations.append({
            "source_id": source_id,
            "source_file": m.get("source_file"),
            "page": m.get("page"),
            "chunk_id": m.get("chunk_id"),
            "passage": document.page_content,
        })
    return citations
