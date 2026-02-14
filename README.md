# 🧠 AI Loan Decision Copilot (Multi-Agent RAG System)

A production-style decision intelligence system that combines Retrieval-Augmented Generation (RAG), multi-agent reasoning, and deterministic policy enforcement to evaluate loan applications.

Unlike standard chatbots, this system prevents hallucinated approvals by integrating an LLM reasoning layer with a rule-based compliance engine.

---

## 🧠 System Architecture

```mermaid
flowchart TD

A[User Request] --> B[FastAPI Backend]

B --> C[RAG Retrieval Layer]
C --> C1[PDF Loader]
C --> C2[Chunking]
C --> C3[Chroma Vector DB]
C --> C4[Ollama Embeddings]

B --> D[Multi-Agent System - CrewAI]

D --> D1[Research Analyst]
D --> D2[Risk Officer]
D --> D3[Compliance Officer]
D --> D4[Manager]

D --> E[Local LLM - Ollama Llama3]

E --> F[Structured Output Validator]

F --> G[Policy Guardrail Engine]

G --> H[Final Decision API Response]
```


---

# What this diagram communicates to recruiters

Without reading code they instantly see:

- RAG architecture ✔
- multi-agent orchestration ✔
- local LLM hosting ✔
- guardrail enforcement ✔
- production API ✔

This screams **GenAI Engineer**, not student.

---

# 🧠 AI Loan Decision Copilot (Multi-Agent RAG System)

A production-style decision intelligence system that combines Retrieval-Augmented Generation (RAG), multi-agent reasoning, and deterministic policy enforcement to evaluate loan applications.

Unlike standard chatbots, this system prevents hallucinated approvals by integrating an LLM reasoning layer with a rule-based compliance engine.
