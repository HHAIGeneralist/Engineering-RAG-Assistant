from src.config import get_settings
from src.ingest import ingest_pdfs


def main() -> None:
    settings = get_settings()
    pdf_files = sorted(settings.data_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {settings.data_dir}")
    count = ingest_pdfs(pdf_files, recreate=True)
    print(f"Finished. Uploaded {count} chunks to '{settings.qdrant_collection}'.")

if __name__ == "__main__":
    main()
