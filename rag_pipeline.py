from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI



def load_or_build_qa_chain():
    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())
    else:
        loaders = [PyPDFLoader(f"data/{f}") for f in os.listdir("data") if f.endswith(".pdf")]
        docs = [doc for loader in loaders for doc in loader.load()]
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
        vectorstore.save_local("faiss_index")
    
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=OpenAI(model="gpt-4"), retriever=retriever, return_source_documents=True)
