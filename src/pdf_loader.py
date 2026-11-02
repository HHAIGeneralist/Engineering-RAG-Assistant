from pathlib import Path
import fitz
from langchain_core.documents import Document


def load_pdf_pages(pdf_path: Path) -> list[Document]:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    pages: list[Document] = []
    with fitz.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf):
            text = page.get_text("text").strip()
            if not text:
                continue
            pages.append(Document(page_content=text, metadata={
                "source_file": pdf_path.name,
                "source_path": str(pdf_path.resolve()),
                "page": page_index + 1,
                "document_id": pdf_path.stem,
            }))
    return pages
