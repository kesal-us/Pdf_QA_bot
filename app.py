import streamlit as st
from utils import load_pdf_from_buffer
from rag_engine import RAGEngine

st.set_page_config(page_title="PDF Q&A")
st.title("PDF Q&A")
st.write("Upload a PDF and ask questions about its content.")

if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()

knowledge_ready = st.session_state.rag.vectordb is not None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Use buffer instead of file path
    docs = load_pdf_from_buffer(uploaded_file.getbuffer())

    if not docs:
        st.error("Could not load any text from this PDF.")
    else:
        st.session_state.rag.build_vector_store(docs)
        st.success("PDF processed and embeddings stored!")
        knowledge_ready = True

if knowledge_ready:
    query = st.text_input("Ask a question about the PDF:")
    if query:
        answer = st.session_state.rag.query(query)
        st.write("**Answer:**")
        st.info(answer)
else:
    st.warning("Please upload and process a PDF first.")
