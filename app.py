import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from rag_pipeline import load_or_build_qa_chain

st.set_page_config(page_title="Clinical Study RAG", layout="wide")

# Load user config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
    
login_info = authenticator.login(location="main")

if login_info is not None:
    name, authentication_status = login_info
else:
    name, authentication_status = None, None


 
authenticator.login(location="main", key="unique_login_key")

if authenticator.authentication_status:
    st.sidebar.success(f" Logged in as: {authenticator.name}")
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
        
elif authenticator.authentication_status is False:
    st.error("❌ Incorrect username or password.")
elif authenticator.authentication_status is None:
    st.info(" Please log in to continue.")
