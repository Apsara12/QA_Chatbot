from ast import While
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from document_loader import load_and_split_docs, load_and_split_docs_from_directory
from vector_store import create_vector_store
from agents.tool_agent import is_valid_email, is_valid_phone, extract_date_fn
from chains.qa_chain import get_qa_chain
from llm import llm
import os


#load documents
while True:
    path = input("Enter the path to the document (PDF/TXT) or a directory: ").strip()
    if not os.path.exists(path):
        print("Path doesn't exist. Please try again.")
        continue
    if os.path.isfile(path) and path.endswith((".pdf", ".txt")):
        chunks = load_and_split_docs(path)
        break
    elif os.path.isdir(path):
        chunks = load_and_split_docs_from_directory(path)
        break
    else:
        print("Invalid path or file type. Please provide a valid PDF or TXT file or a directory containing such files.")

vector_store = create_vector_store(chunks)
qa_chain = get_qa_chain(vector_store.as_retriever())

print("Welcome to the Q&A Bot! Ask anything from the documents and type 'exit' to quit.\n")

while True:
    query = input(" You: ").strip()
    if query.lower() in ["exit", "quit"]:
        print("Thank you for using the Q&A Bot.")
        break

    intent_prompt = f"""
    Classify the user's intent from the following query.
    
    Return only one of:
    - qa — if the user is asking a question to get information from the uploaded document.
    - contact — if the user wants to be contacted, share phone/email/name, or says "call me" etc.
    - appointment — if the user wants to schedule/book a time.
    
    Only reply with one word: qa, contact, or appointment.
    Query: "{query}"
    """

    raw_intent = llm.invoke(intent_prompt)
    intent_str = raw_intent.content.strip().lower()
    #print(f"[DEBUG] Intent output from LLM: {intent_str}")

    if intent_str not in ["qa", "contact","appointment"]:
        print(" Sorry, I am unable to understand that.")
        continue

    if intent_str == "contact":
        print(" Please provide your contact details.")
       
        while True:
            name = input("Name: ").strip()
            if name:
                break
            print("Name cannot be empty.Please enter your name")
        while True:
            phone = input("Phone: ")
            if is_valid_phone.invoke(phone):
                break
            print("Invalid phone number. Please try again.")
        
        while True:
            email = input("Email: ")
            if is_valid_email.invoke(email):
                break
            print("Invalid email address. Please try again.")

        print(f"Thank you {name}, We will call you at {phone} and email you at {email}.")
        continue

    elif intent_str =="appointment":
        date_result = extract_date_fn.invoke(query)
        if date_result == "Invalid date format":
            print("Couldn't extract a valid date.\n")
        else:
            print(f"Your appointment is scheduled for {date_result}.\n")
        continue
    
    else:
        try:
            result = qa_chain.invoke({"question":query, "chat_history": [] })
            print("Bot: ", result["answer"],"\n")

            for i, doc in enumerate(result.get("source_documents",[]),1):
                print(f"\n Retrieved Document {i}:\n{doc.page_content}")
        except Exception as e:
            print(" Failed to answer the question:", str(e))


   