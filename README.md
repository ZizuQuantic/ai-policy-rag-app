Markdown

# AI Policy RAG Assistant

An intelligent, context-aware assistant designed to help employees quickly and accurately query internal corporate policy documents. By combining the power of Large Language Models (LLMs) with a Retrieval-Augmented Generation (RAG) architecture, this system ensures that answers are grounded strictly in the company's official documentation, completely eliminating AI hallucinations.

The application features both a modern, user-friendly **Streamlit web interface** and a lightweight **Terminal/CLI interface** for flexible testing.

---
## Key Features

* **Strict Context Bounding:** The assistant only answers questions using retrieved policy text. If a topic isn't in the provided documents, it honestly declines to answer rather than making up information.
* **Smart Intent Detection (Cost & Speed Optimization):** The application checks user inputs for basic conversational phrases (like "Thank you" or "Thanks"). It intercepts these messages and responds instantly with friendly pre-set replies, saving API token costs and eliminating server lag.
* **Modern LangChain Expression Language (LCEL):** Built using the latest LangChain standards with clean, readable pipe-based (`|`) pipelines for smooth document data flow.
* **Secure Key Management:** Sensitive API credentials are kept safely isolated in a local `.env` file, protecting private keys from being exposed in the source code.

---

## System Prerequisites

* **Python Version:** `Python 3.12.9` (Optimized and fully tested on stable Python 3.12+ environments).
* **Environment:** A local workspace with proper terminal and file read/write permissions.

---

## How the System Works (Project Workflow)

1. **Document Ingestion:** The system scans the data directory for corporate policy files (`.txt`, `.md`, `.pdf`, `.docx`). Texts are read securely using UTF-8 encoding to prevent parsing errors.
2. **Text Chunking & Embedding:** Documents are broken into overlapping text segments and processed through `openai/text-embedding-3-small` via OpenRouter to create highly accurate vector representations.
3. **Local Knowledge Base:** These vectors are saved directly to a local directory using a FAISS vector database, requiring no heavy cloud database setup.
4. **Smart Interception & Retrieval:** * When a user types a message, the app first screens it for quick pleasantries. 
   * If it's a real question, the system searches the FAISS index to pull the top 3 most relevant context chunks.
5. **Answer Generation:** The context and the user's question are sent to the `google/gemma-3-27b-it` model via OpenRouter, which generates a natural, professional summary of the company policy.

---

## Environment Variables Configuration

Before running the application, you must set up your environment variables. Create a file named `.env` in the root directory of the project and add your OpenRouter API keys. 

*Note: Since LangChain's underlying OpenAI wrapper expects an OpenAI key structure, copy your OpenRouter key into both fields to ensure proper integration:*

```env
OPENAI_API_KEY=sk-or-v1-your_actual_openrouter_api_key_here
OPENROUTER_API_KEY=sk-or-v1-your_actual_openrouter_api_key_here

Installation & Setup

Follow these simple steps to set up and run the project on your local machine:
1. Clone the Repository
Bash

git clone [https://github.com/ZizuQuantic/ai-policy-rag-app.git](https://github.com/ZizuQuantic/ai-policy-rag-app.git)
cd ai-policy-rag-app

2. Set Up the Virtual Environment

Create and activate a virtual environment to isolate the project dependencies, then install the required packages:
Bash

python -m venv venv

# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

Execution Guide
Step 1: Ingest Policy Documents
Place your corporate policy documents inside the data/ folder, then run the ingestion script to parse the files and construct your local FAISS vector store:

Bash
python ingest.py

Step 2: Launch the Streamlit Web Application
To chat with your policy assistant via a modern web browser interface, launch the Streamlit app:

Bash
streamlit run gui.py

Step 3: Run via Terminal (Alternative CLI Mode)
If you prefer to interact with the assistant directly inside your command line terminal without opening a browser, use the CLI mode:

Bash
python app.py 

Engineering & Troubleshooting History

During development, several key technical refinements were implemented to improve the stability and performance of the RAG pipeline:

    LangChain Integration Fix: Resolved initial API setup barriers by duplicating the OpenRouter credential mapping to OPENAI_API_KEY. This successfully fulfilled the framework's internal default ecosystem requirements without breaking the connection.

    Modern Syntax Upgrade: Migrated legacy RetrievalQA chains over to modern LangChain Expression Language (LCEL) code structures, resulting in modular, maintainable, and future-proof code.

    Character Encoding Standard: Fixed file-reading exceptions across diverse text formats by standardizing all internal text readers to pure UTF-8 encoding.

    Cost-Efficient Chat Flows: Implemented custom text cleaning and keyword screening inside the UI processing loops to answer basic generic queries locally without hitting external LLM endpoints.