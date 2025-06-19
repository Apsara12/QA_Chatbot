from document_loader import load_and_split_docs
from vector_store import create_vector_store, retrieve_docs
from llm import llm
import re
import dateparser
import os


def is_valid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\+?[1-9]\d{1,14}$", phone)

def extract_date(text):
    date = dateparser.parse(text)
    if date:
        return date.strftime("%Y-%m-%d")
    return None

while True:
    file_path = input("Enter the path to the document (PDF or TXT): ").strip()
    if os.path.exists(file_path) and (file_path.endswith(".pdf") or file_path.endswith(".txt")):
        break
    print("File not found. Please try again.")
chunks = load_and_split_docs(file_path)
vector_store = create_vector_store(chunks)

print("Welcome to the Q&A Bot!")

while True:
    query = input(" You: ")
    if "call me " in query.lower():
        name = input("Name: ")

        while True:
            phone = input("Phone: ")
            if is_valid_phone(phone):
                break
            print("Invalid phone number. Please try again.")

        while True:
            email = input("Email: ")
            if is_valid(email):
                break
            print("Invalid email address. Please try again.")

        print(f"Thank you {name}, We will call you at {phone} and email you at {email}.")
        continue

    if "appointment" in query.lower():
        date = extract_date(query)
        if date:
            print(f"Your appointment is scheduled for {date}.")
        else:
            print("Could not extract a valid date.")

    relevant_docs = retrieve_docs(query, vector_store)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    response = llm.generate_content(f"Context:\n{context}\n\nQuestion: {query}")
    print("Bot: ", response.text)