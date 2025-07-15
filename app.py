import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from rag_pipeline import load_or_build_qa_chain

# Set Streamlit page config
st.set_page_config(page_title="Clinical Study RAG", layout="wide")

# Load config.yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Perform login
login_result = authenticator.login(location="main", key="login_key")

# Handle login state
if login_result is None:
    st.warning("👈 Please enter your username and password.")
else:
    name, authentication_status, username = login_result

    if authentication_status:
        st.sidebar.success(f"🔓 Logged in as: {name}")
        authenticator.logout("Logout", "sidebar")

        # Main content
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
