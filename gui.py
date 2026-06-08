import os
import streamlit as st
import random  # Make sure this has its own line!
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Configuration and Constants
FAISS_INDEX_PATH = "faiss_index"
MODEL_NAME = "google/gemma-3-27b-it"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

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

def initialize_vector_store():
    """Load the locally saved FAISS vector database."""
    try:
        embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=OPENROUTER_BASE_URL,
            model="openai/text-embedding-3-small"
        )
        return FAISS.load_local(
            FAISS_INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        st.error(f"Failed to load FAISS index: {str(e)}")
        return None

def build_rag_chain(vector_store):
    """Construct the modern LCEL RAG pipeline."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Initialize the Gemma 3 model via OpenRouter
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=OPENROUTER_BASE_URL,
        model=MODEL_NAME,
        temperature=0.3
    )
    
    # Professional prompt template defining constraints
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
    # Streamlit Page Setup
    st.set_page_config(page_title="AI Policy RAG Assistant", page_icon="📝", layout="centered")
    st.title("📝 AI Policy RAG Assistant")
    st.subheader("Query internal company policies with zero hallucinations")
    st.write("---")

    # Security Check: Ensure API keys are present in the environment
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        st.error("Missing API Credentials. Please configure your .env file with valid OpenRouter keys.")
        return

    # Initialize backend components
    vector_store = initialize_vector_store()
    if not vector_store:
        st.warning("No knowledge base found. Please run 'python ingest.py' first to index your documents.")
        return
        
    rag_chain = build_rag_chain(vector_store)

    # Initialize chat history state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render previous messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if user_query := st.chat_input("Ask a question about company policies (e.g., Remote Work, Expenses)..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Generate and display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # -------------------------------------------------------------
            # INTERCEPTION: Check for "Thank You" messages first
            # -------------------------------------------------------------
            thank_you_reply = check_for_thanks(user_query)
            
            if thank_you_reply:
                # If they said thank you, display it immediately and save to history
                response_placeholder.markdown(thank_you_reply)
                st.session_state.messages.append({"role": "assistant", "content": thank_you_reply})
            else:
                # Regular RAG Workflow (Only runs if it is an actual policy question)
                with st.spinner("Searching documents and formulating answer..."):
                    try:
                        response = rag_chain.invoke(user_query)
                        response_placeholder.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"An error occurred while generating the response: {str(e)}"
                        response_placeholder.markdown(error_msg)

if __name__ == "__main__":
    main()