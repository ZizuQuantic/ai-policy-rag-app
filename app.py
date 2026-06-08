import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import random  # Make sure this has its own line!

# Keywords that look like a "Thank you" message
THANK_YOU_KEYWORDS = [
    "thank you", "thanks", "thx", "thank you so much", 
    "thank you!", "appreciate it", "many thanks"
]

# Single-line responses for your RAG Assistant
THANK_YOU_RESPONSES = [
    "You are very welcome! Please let me know if you have any other questions about the policy.",
    "I am glad I could be of assistance. Let me know if you need help finding anything else!",
    "Happy to help! Feel free to ask if any other policy details require clarification.",
    "My pleasure! I am here whenever you need further assistance with our documentation.",
    "No problem at all! Happy to help. 😊"
]

def check_for_thanks(user_input: str) -> str | None:
    """
    Checks if the user input is a 'thank you' phrase.
    Returns a random friendly response if true, or None if it's a regular query.
    """
    # Clean the input: lowercase and remove basic punctuation trailing spaces
    cleaned_input = user_input.lower().strip().strip("!.,")
    
    if cleaned_input in THANK_YOU_KEYWORDS:
        return random.choice(THANK_YOU_RESPONSES)
    
    return None

# Load environment variables
load_dotenv()

FAISS_INDEX_PATH = "faiss_index"
MODEL_NAME = "google/gemma-3-27b-it"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

def initialize_rag_system():
    """Initializes the embeddings, loads the FAISS index, and builds the LCEL chain."""
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Missing API credentials in .env file.")
        return None

    if not os.path.exists(FAISS_INDEX_PATH):
        print(f"Error: Vector store store '{FAISS_INDEX_PATH}' not found. Please run 'python ingest.py' first.")
        return None

    # Initialize embeddings matching the ingestion setup
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=OPENROUTER_BASE_URL,
        model="openai/text-embedding-3-small"
    )

    # Load the local FAISS database
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Initialize the Gemma 3 model via OpenRouter
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=OPENROUTER_BASE_URL,
        model=MODEL_NAME,
        temperature=0.3
    )

    # Standardized prompt template defining constraints
    prompt_template = """You are a helpful and professional corporate policy assistant. 
Use the following pieces of retrieved context to answer the user's question. 
If the answer cannot be found in the context, strictly reply with: "I'm sorry, but I cannot find that information in the company policy documents." Do not try to make up an answer.

Context:
{context}

Question: {question}
Answer:"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Modern LangChain Expression Language (LCEL) Chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def main():
    print("Initializing AI Policy RAG System...")
    rag_chain = initialize_rag_system()
    
    if not rag_chain:
        print("Initialization failed. Exiting.")
        return

    print("\nSystem ready! Type your question below (or type 'exit' to quit).")
    print("-" * 60)

    while True:
        try:
            user_query = input("\nAsk a policy question: ").strip()
            if not user_query:
                continue
            if user_query.lower() in ['exit', 'quit']:
                print("Exiting RAG System. Goodbye!")
                break

            # -------------------------------------------------------------
            # STEP 3 INTERCEPTION: Check for "Thank You" messages first
            # -------------------------------------------------------------
            thank_you_reply = check_for_thanks(user_query)
            
            if thank_you_reply:
                # If they said thank you, print the phrase instantly and skip the LLM
                print(f"\nAnswer: {thank_you_reply}")
                print("-" * 60)
                continue
            # -------------------------------------------------------------

            # This part only runs if they didn't say "Thank You"
            print("Searching context and generating answer...")
            response = rag_chain.invoke(user_query)
            print(f"\nAnswer: {response}")
            print("-" * 60)
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()