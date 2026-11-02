import streamlit as st
from src.config import get_settings
from src.rag_pipeline import answer_question

s = get_settings()
st.set_page_config(page_title=s.app_name, page_icon="🔧", layout="wide")
st.title(s.app_name)
st.caption("Query engineering manuals and papers using a local open-weight LLM with page-level evidence.")
st.warning("Verify safety-critical answers against the original document. This tool does not replace engineering judgement or manufacturer instructions.")
question = st.text_area("Ask a question", placeholder="What checks are required before startup?", height=110)
top_k = st.slider("Passages to retrieve", 3, 12, s.retrieval_top_k)
if st.button("Ask the documents", type="primary"):
    if not question.strip():
        st.error("Enter a question.")
    else:
        try:
            with st.spinner("Retrieving evidence and generating the answer..."):
                result = answer_question(question, top_k)
            st.subheader("Answer")
            st.markdown(result["answer"])
            st.subheader("Supporting evidence")
            if not result["citations"]:
                st.info("No valid citations were returned.")
            for citation in result["citations"]:
                label = f'{citation["source_id"]}: {citation["source_file"]}, page {citation["page"]}'
                with st.expander(label):
                    st.write(citation["passage"])
                    st.caption(f'Chunk ID: {citation["chunk_id"]}')
        except Exception as exc:
            st.error(f"Application error: {exc}")
