from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from src.citations import cited_sources, format_sources
from src.config import get_settings
from src.prompts import SYSTEM_PROMPT


def get_llm() -> ChatOllama:
    s = get_settings()
    return ChatOllama(
        model=s.ollama_chat_model,
        base_url=s.ollama_base_url,
        temperature=0,
        validate_model_on_init=True,
    )


def generate_answer(question: str, documents) -> dict:
    formatted, source_map = format_sources(documents)
    response = get_llm().invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Question:\n{question}\n\nSources:\n{formatted}"),
    ])
    answer = response.content if isinstance(response.content, str) else str(response.content)
    return {"answer": answer, "citations": cited_sources(answer, source_map)}
