# 📝 AI Policy RAG Assistant

A production-ready Retrieval-Augmented Generation (RAG) system built to query internal corporate policy documents with zero hallucinations. The system leverages LangChain (LCEL), OpenRouter, Google's Gemma 3 model, and FAISS to provide precise, context-bounded answers through a modern Streamlit web interface.

---

## 🛠️ System Prerequisites

* **Python Version:** `Python 3.12.9` (Tested and fully optimized for Python 3.12+ stable package environments).
* **Environment Configuration:** Secure local credential storage via a `.env` file to protect private API keys from being exposed.

---

## 🚀 Project Workflow

1. **Ingestion & Embedding:** Document parsers scan the local directory for policy documents (`.txt`, `.md`, `.pdf`, `.docx`). The text is split into chunks and converted into vector math using `openai/text-embedding-3-small`.
2. **Local Vector Database:** The embeddings are saved locally using a FAISS vector database.
3. **Retrieval & Augmentation:** When a user asks a question, the top 3 most relevant document chunks are retrieved and injected into a strict prompt template.
4. **Generation:** The `google/gemma-3-27b-it` model processes the context. If the answer is present, it summarizes it; if not, it honestly states that the information cannot be found, preventing hallucinations.

---

## ⚙️ Environment Variables Configuration

For security reasons, API keys must never be hardcoded into the source scripts. To configure credentials, a file named `.env` must be created in the root directory of the project with the following structure:

```env
OPENAI_API_KEY=sk-or-v1-your_actual_openrouter_api_key_here
OPENROUTER_API_KEY=sk-or-v1-your_actual_openrouter_api_key_here


📦 Installation & Setup

Follow these steps to deploy and run the project locally:
1. Clone the Repository
Bash

git clone [https://github.com/YOUR_USERNAME/ai-policy-rag-app.git](https://github.com/YOUR_USERNAME/ai-policy-rag-app.git)
cd ai-policy-rag-app

2. Set Up the Virtual Environment (Python 3.12.9)

Initialize a virtual environment and install the required dependencies listed in the requirements.txt file:
Bash

python -m venv .venv

# On Windows (Command Prompt):
.venv\Scripts\activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

🏃 Execution Guide
Step 1: Ingest Policy Documents

Place all corporate policy documents inside the data/ folder, then run the ingestion script to build and update the local vector database:
Bash

python ingest.py

Step 2: Launch the Streamlit Web UI

Execute the following command to start the interactive web application interface for querying the policies:
Bash

streamlit run gui.py

Step 3: Run via Terminal (Optional CLI Mode)

Alternatively, the system can be queried directly inside the terminal command line without launching the web browser:
Bash

python app.py

🧠 Development & Troubleshooting History

    Missing Credentials Configuration: Resolved by duplicating the OpenRouter credential mapping to OPENAI_API_KEY to satisfy LangChain's internal default ecosystem requirements.

    ModuleNotFoundError & Deprecation Handling: Upgraded legacy RetrievalQA chains to the modern LangChain Expression Language (LCEL) syntax using the pipe (|) operator.

    Framework Imports Standardized: Consolidated all Streamlit interface deployments under import streamlit as st.

    Encoding Optimization: Standardized all internal file readers to pure UTF-8 encoding to prevent parsing errors across diverse document formats.