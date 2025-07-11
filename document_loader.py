from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_and_split_docs(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    return splitter.split_documents(docs)

def load_and_split_docs_from_directory(directory_path):
    all_chunks = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.lower().endswith((".pdf",".txt")):
            try:
                chunks = load_and_split_docs(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    return all_chunks