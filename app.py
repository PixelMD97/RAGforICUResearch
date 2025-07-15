import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from rag_pipeline import load_or_build_qa_chain

st.set_page_config(page_title="Clinical Study RAG", layout="wide")

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Perform login (with unique key)
name, authentication_status, username = authenticator.login(location="main", key="login")

# Main logic
if authentication_status:
    st.sidebar.success(f"👤 Logged in as: {name}")
    authenticator.logout("Logout", "sidebar")

    st.title("Clinical Study Chatbot (RAG)")
    query = st.text_input("Ask a question about the study documents:")
    if query:
        qa_chain = load_or_build_qa_chain()
        result = qa_chain({"query": query})
        st.write(result['result'])
        with st.expander("Sources"):
            for doc in result["source_documents"]:
                st.markdown(f"📄 {doc.metadata.get('source')} — Page {doc.metadata.get('page', '?')}")
elif authentication_status is False:
    st.error("❌ Incorrect username or password.")
elif authentication_status is None:
    st.info("👈 Please enter your username and password.")
