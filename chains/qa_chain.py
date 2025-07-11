from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from llm import llm

def get_qa_chain(retriever):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = retriever,
        memory = memory,
        return_source_documents = False,
    )
    return chain
