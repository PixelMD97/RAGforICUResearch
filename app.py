import streamlit as st
from rag_pipeline import load_or_build_qa_chain
import os
from datetime import datetime

# --- Page setup
st.set_page_config(page_title="Clinical Study Chatbot", layout="wide")

# --- Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Title and intro
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🩺 Clinical Study Chatbot (RAG)</h1>",
    unsafe_allow_html=True
)

st.markdown("💬 **Stelle eine Frage zu den Studiendokumenten:**")

# --- Input field
query = st.text_input(" ", placeholder="z. B. Welche Patienteninfo wird benötigt aus EPIC?")

# --- Example questions
with st.expander("🔍 Beispiel-Fragen anzeigen"):
    st.markdown(
        "- Was ist die Definition von Kreislaufversagen?\n"
        "- Welche Patienteninfo wird benötigt aus EPIC?\n"
        "- Wer ist der PI der Studie?\n"
        "- Welche Assessments werden erhoben?\n"
        "- Wie viele Patienten sollen eingeschlossen werden?"
    )

# --- Handle new question
if query:
    qa_chain = load_or_build_qa_chain()
    result = qa_chain({"query": query})

    st.session_state.chat_history.append({
        "question": query,
        "answer": result["result"],
        "sources": result.get("source_documents", []),
        "timestamp": datetime.now().strftime("%H:%M")
    })

# --- Display chat history (reversed)
for entry in reversed(st.session_state.chat_history):
    timestamp = entry.get("timestamp", "--:--")

    # Question bubble
    st.markdown(
        f"""
        <div style='display: flex; align-items: flex-start; margin-bottom: 1rem;'>
            <div style='font-size: 1.5rem; margin-right: 0.5rem;'>🧑‍⚕️</div>
            <div style='background-color: #ecf0f1; padding: 0.6rem 1rem; border-radius: 0.5rem; max-width: 80%;'>
                <b>Du ({timestamp}):</b><br>{entry["question"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Answer bubble
    st.markdown(
        f"""
        <div style='display: flex; align-items: flex-start; margin-bottom: 1rem;'>
            <div style='font-size: 1.5rem; margin-right: 0.5rem;'>🤖</div>
            <div style='background-color: #d6eaf8; padding: 0.6rem 1rem; border-radius: 0.5rem; max-width: 80%;'>
                <b>RAG-Bot:</b><br>{entry["answer"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sources
    if entry["sources"]:
        with st.expander("📚 Quellen anzeigen"):
            for doc in entry["sources"]:
                metadata = doc.metadata
                source = metadata.get("source", "Unbekannt")
                page = metadata.get("page", "?") + 1
                filename = os.path.basename(source).replace(".pdf", "").replace("-", " ").title()
                st.markdown(f"📄 **{filename}**, Seite {page}")

# --- Feedback section (after each response)
if query:
    st.markdown("#### War die Antwort hilfreich?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Ja", key=f"yes_{query}"):
            st.success("Danke für dein Feedback!")
    with col2:
        if st.button("👎 Nein", key=f"no_{query}"):
            st.warning("Wir arbeiten daran, es zu verbessern.")
