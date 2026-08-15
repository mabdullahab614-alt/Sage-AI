# Sage AI — Intelligent Document & Code Assistant

A single-page chatbot that combines general conversation, RAG-based document Q&A
(PDF/Word/Excel/CSV/TXT), and Python code generation + execution.

## Setup

```bash
pip install -r requirements.txt
```

Get a free Groq API key: https://console.groq.com/keys

```bash
export GROQ_API_KEY="your-key-here"      # macOS/Linux
setx GROQ_API_KEY "your-key-here"        # Windows
```

## Run

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually http://localhost:8501).

## What's implemented (maps to the PRD)

| PRD Feature | Status | File |
|---|---|---|
| General Chat | ✅ | `utils/llm.py`, `app.py` |
| Multi-Document Upload | ✅ | `utils/document_parser.py` |
| RAG Q&A | ✅ | `utils/rag.py` (ChromaDB + sentence-transformers, local) |
| Code Generation | ✅ | `utils/llm.py` (extracts ```python blocks) |
| Code Execution | ✅ (best-effort sandbox) | `utils/code_executor.py` |
| Chat Memory | ✅ | Streamlit `session_state` |
| File Type Auto-Detection | ✅ | `utils/document_parser.py` |
| Error Handling | ✅ | try/except + custom exceptions throughout |

## Known limitations / where to harden before real deployment

1. **Code execution is NOT a hard security boundary.** It uses a subprocess
   with CPU/memory/process-count limits (`resource.setrlimit`) and a timeout,
   which stops runaway scripts and fork bombs, but does **not** provide real
   network or filesystem isolation. For production, swap `utils/code_executor.py`
   to call **E2B** (https://e2b.dev) or **Judge0** (https://judge0.com) instead
   — both have free tiers and run code in a truly isolated container/VM. The
   swap point is marked with a comment in that file.
2. **Chunking** defaults to 800 chars / 150 overlap — tune per document type
   if RAG answers feel off (tables and code benefit from larger chunks).
3. **No file size/page limit enforced yet** — the PRD calls for capping
   documents at ~50 pages; add a check in `app.py`'s upload handler.
4. **ChromaDB is local/persistent to `./chroma_store`** — fine for a single-user
   demo; for the "no login, single-page" MVP this matches the PRD's non-goals
   (no multi-user persistent history).
5. Deploy to Hugging Face Spaces by pushing these files + a `Spaces`-flavored
   `README.md` header (`sdk: streamlit`) and setting `GROQ_API_KEY` as a
   Space secret.

## Project structure

```
sage-ai/
├── app.py                  # Streamlit UI + orchestration
├── requirements.txt
├── utils/
│   ├── llm.py               # Groq chat completion + code block extraction
│   ├── document_parser.py   # PDF/Word/Excel/CSV/TXT → text
│   ├── rag.py                # chunking, embedding, ChromaDB retrieval
│   └── code_executor.py      # sandboxed(ish) Python execution
└── README.md
```
