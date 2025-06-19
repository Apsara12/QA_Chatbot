from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)

def retrieve_docs(query, vector_store, max_total_chars=3000):
    results = vector_store.similarity_search(query, k=8)

    #reduce context if too long
    total_chars = 0
    limited_results = []
    for doc in results:
        total_chars += len(doc.page_content)
        if total_chars > max_total_chars:
            break
        limited_results.append(doc)
    return limited_results
