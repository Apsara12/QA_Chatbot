from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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