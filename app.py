import streamlit as st
from rag_pipeline import load_or_build_qa_chain

st.set_page_config(page_title="Clinical Study RAG", layout="wide")

st.title("Clinical Study Chatbot (RAG)")

query = st.text_input("Ask a question about the study documents:")

if query:
    qa_chain = load_or_build_qa_chain()
    result = qa_chain({"query": query})

    st.write(result['result'])

    with st.expander("Sources"):
        for doc in result["source_documents"]:
            st.markdown(f"📄 {doc.metadata.get('source')} — Page {doc.metadata.get('page', '?')}")
            
            
            
