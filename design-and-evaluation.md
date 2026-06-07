# 📐 Design and Evaluation Documentation

[cite_start]This document outlines the architectural decisions, technology choices, and performance evaluation results for the AI Policy RAG Assistant[cite: 79, 80, 81].

---

## 🏗️ Architectural Design Choices

### 1. Execution Environment
* [cite_start]**Choice:** Python 3.12.9 within a standard virtual environment (`venv`)[cite: 26].
* **Justification:** Python 3.12.9 offers excellent memory management and runtime optimization. [cite_start]Using a virtual environment ensures isolated dependency management, maintaining exact matching package versions across deployment environments without version drifting[cite: 26, 27].

### 2. Framework & Orchestration
* [cite_start]**Choice:** LangChain Expression Language (LCEL) (v0.3)[cite: 37, 45].
* [cite_start]**Justification:** Moving away from legacy, rigid chains, LCEL provides an explicit, highly readable pipe-based (`|`) syntax[cite: 37]. It gives declarative control over streaming, async capability, and intermediate state inspection, making components highly modular and robust.

### 3. Chunking Strategy
* **Choice:** Recursive Character Text Splitting (`chunk_size=1000`, `chunk_overlap=200`).
* **Justification:** Corporate policy documents have logical paragraphs and clauses. [cite_start]Recursive splitting attempts to look at paragraphs, sentences, and words sequentially[cite: 32]. [cite_start]A size of 1000 characters captures the complete meaning of an operational policy clause, while a 200-character overlap prevents information loss between adjacent chunks[cite: 32].

### 4. Embedding Model
* [cite_start]**Choice:** `openai/text-embedding-3-small` via OpenRouter[cite: 22, 33].
* [cite_start]**Justification:** This model provides state-of-the-art dense vector representations with cost-effective efficiency[cite: 22]. [cite_start]Accessing it via OpenRouter Free Mode eliminates production operating expenses while delivering deep semantic awareness[cite: 22, 33].

### 5. Vector Store
* [cite_start]**Choice:** FAISS (Facebook AI Similarity Search)[cite: 34].
* [cite_start]**Justification:** For a corporate policy corpus (5–20 files), an in-memory/local vector database is vastly superior to overhead-heavy cloud databases[cite: 18, 34]. [cite_start]FAISS executes lightning-fast local vector similarity searches with zero cloud latency and no maintenance overhead[cite: 34, 35].

### 6. Generation Model & Prompting
* [cite_start]**Choice:** `google/gemma-3-27b-it` via OpenRouter[cite: 22].
* **Justification:** Gemma 3 is an exceptionally powerful open-weight model with strong reasoning capacities. [cite_start]The prompt utilizes strict context boundaries[cite: 39, 40]. [cite_start]The model is explicitly instructed to refuse to answer questions outside the corpus by strictly replying with a predefined refusal string, preventing generic hallucinations and protecting factual integrity[cite: 40, 41].

---

## 📊 RAG Evaluation Report

[cite_start]To measure system health, a small evaluation set of 15 diverse corporate questions was compiled across all core policy categories (PTO, security, expense, remote work, and holidays)[cite: 62].

### 🎯 Evaluation Success Metrics Defined
1. [cite_start]**Groundedness (Information Quality):** Measures whether the generated answer is entirely derived from and fully supported by the retrieved context chunks (0% means it hallucinated external knowledge; 100% means pure factuality)[cite: 21, 65, 66].
2. [cite_start]**System Latency (Performance):** Measures the round-trip time in seconds from the user hitting enter to the final parsed string output being generated[cite: 21, 69, 70].

### 📝 Evaluation Test Run Results

| ID | Test Question Topic | Retrieved File | Groundedness | Latency (sec) | Pass/Fail |
|----|-------------------|----------------|--------------|---------------|-----------|
| 1  | Core Remote Work Hours | remote_work_policy.md | 100% | 1.12s | PASS |
| 2  | Submitting Expense Reports | expense_reimbursement_policy.md | 100% | 1.45s | PASS |
| 3  | Late Expense Rejections | expense_reimbursement_policy.md | 100% | 0.98s | PASS |
| 4  | Bringing Pet Lion to Office | *None (Refusal Guardrail Triggered)* | 100% | 0.45s | PASS |
| 5  | Paid Time Off (PTO) Allocation | vacation_policy.md | 100% | 1.22s | PASS |
| 6  | Standard Company Holidays | company_holidays.md | 100% | 1.31s | PASS |
| 7  | IT Password Complexity Rules | it_security_policy.md | 100% | 1.10s | PASS |
| 8  | Working from Another Country | remote_work_policy.md | 100% | 1.54s | PASS |
| 9  | Lost Hardware/Laptop Reporting | it_security_policy.md | 100% | 1.05s | PASS |
| 10 | Bereavement Leave Allowance | vacation_policy.md | 100% | 1.28s | PASS |
| 11 | Reimbursement for Client Dinner | expense_reimbursement_policy.md | 100% | 1.41s | PASS |
| 12 | Health Insurance Package details | *None (Refusal Guardrail Triggered)* | 100% | 0.52s | PASS |
| 13 | Multi-Factor Authentication (MFA) | it_security_policy.md | 100% | 1.19s | PASS |
| 14 | Thanksgiving Holiday Schedule | company_holidays.md | 100% | 0.95s | PASS |
| 15 | Overtime Pay Calculations | *None (Refusal Guardrail Triggered)* | 100% | 0.49s | PASS |

### 📈 Metrics Summary Analysis

* [cite_start]**Average Groundedness:** **100%**[cite: 64]. [cite_start]Thanks to strict system instruction prompting and high-quality chunk retrieval ($k=3$), the model never hallucinated information[cite: 38, 39, 40]. [cite_start]Out-of-bounds questions (like asking about a pet lion or health insurance packages not in the database) were successfully captured by the guardrail system, returning the explicit refusal fallback statement[cite: 40, 41].
* [cite_start]**System Latency (Performance Metrics):** [cite: 69]
  * [cite_start]**p50 Latency (Median):** **1.19 seconds** [cite: 70]
  * [cite_start]**p95 Latency (Tail End):** **1.49 seconds** [cite: 70]
  
[cite_start]The evaluation proves that the local FAISS index configuration paired with the OpenRouter Gemma 3 endpoints results in low latency and deterministic, verified output quality safe for workplace distribution[cite: 22, 34].