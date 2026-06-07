import os
import streamlit as st
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