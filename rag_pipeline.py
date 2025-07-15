import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI


def load_or_build_qa_chain():
    # Use OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Check if FAISS index already exists
    if os.path.exists("faiss_index"):
        # IMPORTANT: allow_dangerous_deserialization must be True to avoid ValueError
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        # Load all PDFs from the "data/" folder
        loaders = [PyPDFLoader(f"data/{f}") for f in os.listdir("data") if f.endswith(".pdf")]
        docs = [doc for loader in loaders for doc in loader.load()]

        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # Embed and store in FAISS
        vectorstore = FAISS.from_documents(chunks, embeddings)

        # Save index to disk
        vectorstore.save_local("faiss_index")

    # Build retriever and return a QA chain
    retriever = vectorstore.as_retriever()

    return RetrievalQA.from_chain_type(
        llm=OpenAI(model="gpt-4"),
        retriever=retriever,
        return_source_documents=True
    )
