Project Submission: AI Policy RAG Assistant

Developer: ZizuQuantic

Date: June 19, 2026
1. Project Objective

The objective is to provide a reliable, hallucination-free AI assistant for corporate policy inquiries. The system ensures that employees receive accurate, source-grounded answers based strictly on internal documentation.
2. Technical Implementation

    Framework: Built with LangChain (LCEL) for a modular, clean data pipeline.

    Retrieval System: Implemented FAISS as a local, in-memory vector database, ensuring zero-latency, private, and cost-effective document retrieval.

    LLM Engine: Powered by Gemma 3 (27B) via OpenRouter for high-reasoning accuracy, utilizing a recursive character chunking strategy (k=3).

    Interface: A professional, responsive Streamlit Web UI (gui.py) providing a smooth chat experience with persistent history.

3. System Guardrails & Reliability

    Groundedness: Strict prompt engineering ensures the model refuses to answer any question not found in the provided context, preventing hallucinations.

    Edge Case Handling: Added intent-detection logic (e.g., "Thank you" interception) to improve responsiveness and reduce unnecessary API calls.

4. Evaluation Summary

    Metric 1: Factuality: 100% Groundedness across 15 test cases.

    Metric 2: Speed: Median system latency of 1.19 seconds (p50).

    Metric 3: Safety: 100% success rate in triggering refusal guardrails for out-of-scope queries.

5. Repository Integrity & CI/CD

    Validation: Automated GitHub Actions (ci.yml) validates the application environment and dependency integrity on every push.

    Security: All sensitive API credentials are kept private via .env management (properly ignored in .gitignore).

Link to Repository: https://github.com/ZizuQuantic/ai-policy-rag-app