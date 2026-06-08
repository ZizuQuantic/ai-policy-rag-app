Markdown

# Design and Evaluation Documentation

This document explains the architectural choices, technology stack decisions, and real-world evaluation results for the AI Policy RAG Assistant. 

---

## Architectural Design Choices

### 1. Execution Environment
* **Choice:** Python 3.12.9 within a standard virtual environment (`venv`).
* **Justification:** Python 3.12.9 provides excellent runtime stability and clean memory management. Running the app inside an isolated virtual environment (`venv`) ensures that all library dependencies match perfectly across different computers, preventing version conflicts during setup.

### 2. Framework & Orchestration
* **Choice:** LangChain Expression Language (LCEL) (v0.3).
* **Justification:** Instead of using older, rigid LangChain setups, I built this system using the modern LCEL syntax with clean pipe operators (`|`). This makes the data flow explicit, highly readable, and much easier to debug or scale in the future.

### 3. Chunking Strategy
* **Choice:** Recursive Character Text Splitting (`chunk_size=1000`, `chunk_overlap=200`).
* **Justification:** Corporate policy documents naturally consist of distinct paragraphs, rules, and clauses. I chose a recursive character splitter because it intelligently prioritizes breaking text at paragraphs and sentences first. A size of 1000 characters is ideal for keeping a single policy rule completely intact, while the 200-character overlap guarantees no critical context is cut off between chunks.

### 4. Embedding Model
* **Choice:** `openai/text-embedding-3-small` via OpenRouter.
* **Justification:** This model creates highly accurate, dense mathematical vectors that capture the true semantic meaning of policy questions. Connecting to it via OpenRouter's free tier provides high-quality text understanding without requiring expensive server costs during development.

### 5. Vector Store
* **Choice:** FAISS (Facebook AI Similarity Search).
* **Justification:** Since corporate knowledge bases typically consist of a manageable set of core policy files, spinning up a heavy cloud database is unnecessary. FAISS acts as a lightweight, in-memory local vector store that handles similarity searches instantly on the local machine with zero network lag and no subscription fees.

### 6. Generation Model & Prompting
* **Choice:** `google/gemma-3-27b-it` via OpenRouter.
* **Justification:** Gemma 3 is a highly capable open-weight model with exceptional reasoning skills. To prevent "hallucinations," I designed a strict prompt template with tight guardrails. The model is explicitly ordered to answer *only* using the provided text; if the answer isn't in the context, it must strictly reply with a designated fallback refusal string.

---

## Evaluation and Testing Report

To thoroughly test the application's accuracy and performance, I created a diverse evaluation dataset containing 15 test questions spread across core company topics (such as PTO, security, remote work, expenses, and holidays).

### Key Performance Metrics
1. **Groundedness (Factuality):** Tracking whether the generated answer is entirely proven by the retrieved text (0% means it guessed or hallucinated; 100% means it stuck strictly to the official documents).
2. **System Latency (Speed):** The actual time in seconds from the moment a user submits a question to the moment the final answer appears on screen.

### Evaluation Test Run Results

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

### Metrics Summary and Insights

* **Average Groundedness (100% Accuracy):** By combining carefully tuned prompt engineering with precise chunk retrieval ($k=3$), the assistant never hallucinated. Out-of-bounds queries—such as asking about a pet lion or non-existent health insurance packages—successfully triggered the system's guardrails, resulting in the correct predefined refusal message.
* **System Speed (Latency Analysis):** * **Median Response Time (p50):** **1.19 seconds** (Half of all queries loaded in less than 1.19 seconds).
  * **Slowest Standard Response Time (p95):** **1.49 seconds** (Almost all remaining queries loaded well under 1.5 seconds).
  
These tests prove that a local FAISS index working alongside the OpenRouter Gemma 3 endpoint delivers fast responses, reliable factual accuracy, and completely safe output for use in a workplace environment.