Markdown

# AI Tooling Documentation

In line with academic integrity and project guidelines, this document describes how conversational AI assistants were utilized as development partners to design, build, refactor, and document this RAG application.

---

## AI Tools Utilized & Core Workflow

* **Primary AI Collaborator:** Gemini (Google DeepMind) and ChatGPT 5.5
* **Development Strategy:** Collaborative human-guided engineering. The AI was used as an expert coding partner to brainstorm architecture design choices, resolve framework deprecation issues, generate documentation, and help review code logic.

---

## What Worked Exceptionally Well

1. **Modern LCEL Refactoring:** Early versions of the project ran into issues because older LangChain components (like `RetrievalQA`) are now outdated. The AI assistant helped guide the transition of both `app.py` and `gui.py` into clean, modern LangChain Expression Language (LCEL) using pipe (`|`) operators, making the data flow predictable and stable.
   
2. **Environment & Dependency Fixes:** Setting up the project on **Python 3.12.9** required careful version management. The AI helped troubleshoot package issues and pointed out that LangChain's underlying engine requires duplication of the OpenRouter key into an `OPENAI_API_KEY` field, which solved a major connection roadblock.

3. **Guardrail Coding & Logic Improvements:** The AI helped write a strict prompting strategy to lock down the model's responses to the local FAISS index. Furthermore, during UI refinement, we successfully integrated an inline keyword interception system to capture basic phrases like "Thank you" and reply instantly, keeping the app fast and reducing unnecessary API usage.

4. **Professional Polish & Standardization:** The AI was highly effective in polishing all system readmes, user manuals, and technical notes into clear, professional corporate English that meets the required academic presentation standards.

---

## Limitations and Human Interventions Required

* **API Key Security Oversight:** Initial code templates suggested by the AI included simple placeholders that could lead to hardcoding API keys. I intervened to strictly enforce a `.env` file architecture to keep private keys safe and out of the main code.
* **Outdated Python Environment Targets:** The AI occasionally suggested older library configurations tailored for Python 3.10. Because I am explicitly developing on Python 3.12.9, I had to manually adjust and correct the dependencies to ensure exact runtime alignment.
* **Logical Flow Fine-Tuning:** While the AI provided excellent generic UI code snippets, I had to carefully place the intent-detection logic (the "Thank you" blocker) in the correct Streamlit chat loop layout so that responses render beautifully without breaking the conversational history state.

---

## Conclusion on AI-Assisted Engineering

Using AI as a development partner turned what could have been hours of syntax-hunting and debugging into a high-level software design task. By maintaining strict human oversight and double-checking every line of code, the final application achieved a fully operational, stable state while maintaining complete academic honesty and transparency.