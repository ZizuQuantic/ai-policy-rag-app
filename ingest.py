import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"
FAISS_INDEX_PATH = "faiss_index"

def load_documents_from_folder(folder_path):
    documents = []
    
    if not os.path.exists(folder_path):
        print(f"Error: The directory '{folder_path}' does not exist.")
        return documents

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            # Added support for .md files alongside .txt, .pdf, and .docx
            if ext in ['.txt', '.md']:
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
                print(f"Successfully loaded: {filename}")
            elif ext == '.pdf':
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                print(f"Successfully loaded: {filename}")
            elif ext == '.docx':
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
                print(f"Successfully loaded: {filename}")
            else:
                print(f"Skipped unsupported file format: {filename}")
        except Exception as e:
            print(f"Failed to load {filename}: {str(e)}")
            
    return documents

def main():
    print("STARTING RAG SYSTEM - INGESTION PROCESS")
    
    print("Loading documents...")
    raw_documents = load_documents_from_folder(DATA_DIR)
    
    if not raw_documents:
        print("No documents found to process. Exiting.")
        return

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(raw_documents)
    print(f"Created {len(docs)} text chunks.")

    print("Initializing embedding model via OpenRouter...")
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="openai/text-embedding-3-small"
    )

    print("Building and saving FAISS vector database locally...")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(FAISS_INDEX_PATH)
    
    print("Ingestion complete! faiss_index has been successfully updated.")

if __name__ == "__main__":
    main()