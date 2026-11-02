from src.generation import generate_answer
from src.retrieval import retrieve_documents


def answer_question(question: str, top_k: int | None = None) -> dict:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    documents = retrieve_documents(question, top_k)
    if not documents:
        return {"answer": "I could not find sufficient evidence in the selected documents.", "citations": []}
    return generate_answer(question, documents)
