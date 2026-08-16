"""
Sage AI — Intelligent Document & Code Assistant
Built by Abdullah Javed.

Single-page Streamlit app: general chat + RAG over uploaded docs + code gen/execution.
"""

import streamlit as st

from utils.document_parser import parse_document, UnsupportedFileTypeError, EmptyDocumentError
from utils.rag import RAGStore, build_rag_prompt
from utils.llm import chat_completion, extract_python_code_blocks
from utils.code_executor import execute_python
from utils.theme import inject_theme, render_empty_state, PAGE_TITLE, PAGE_ICON

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
inject_theme(st)


# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role": ..., "content": ...}]
if "rag_store" not in st.session_state:
    st.session_state.rag_store = RAGStore()
if "uploaded_filenames" not in st.session_state:
    st.session_state.uploaded_filenames = []


# ---------- Sidebar: document upload ----------
with st.sidebar:
    st.markdown("### 🌿 Sage AI")
    st.write("")

    st.markdown('<p class="sage-eyebrow">Documents</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "PDF, Word, Excel, CSV, or TXT",
        type=["pdf", "docx", "xlsx", "xls", "csv", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        for uf in uploaded_files:
            if uf.name in st.session_state.uploaded_filenames:
                continue
            try:
                with st.spinner(f"Reading {uf.name}..."):
                    parsed = parse_document(uf)
                    num_chunks = st.session_state.rag_store.add_document(
                        parsed["filename"], parsed["text"]
                    )
                st.session_state.uploaded_filenames.append(uf.name)
                st.success(f"{uf.name} indexed — {num_chunks} chunks ready")
            except UnsupportedFileTypeError as e:
                st.error(str(e))
            except EmptyDocumentError as e:
                st.warning(str(e))
            except Exception as e:
                st.error(f"Couldn't process {uf.name}: {e}")

    if st.session_state.uploaded_filenames:
        st.markdown('<p class="sage-eyebrow" style="margin-top:0.8rem;">Indexed</p>', unsafe_allow_html=True)
        for fn in st.session_state.uploaded_filenames:
            st.markdown(f"📄 {fn}")
        if st.button("Clear documents", use_container_width=True):
            st.session_state.rag_store.clear()
            st.session_state.uploaded_filenames = []
            st.rerun()

    st.divider()
    use_rag = st.toggle(
        "Ground answers in documents",
        value=bool(st.session_state.uploaded_filenames),
        help="When on, questions are answered using retrieved document context.",
    )

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------- Main chat area ----------
if not st.session_state.messages:
    render_empty_state(st)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Offer to run any python code blocks found in past assistant messages
        if msg["role"] == "assistant":
            code_blocks = extract_python_code_blocks(msg["content"])
            for i, code in enumerate(code_blocks):
                key = f"run_{id(msg)}_{i}"
                if st.button(f"▶ Run code block {i + 1}", key=key):
                    with st.spinner("Executing..."):
                        result = execute_python(code)
                    if result["success"]:
                        st.code(result["stdout"] or "(no output)", language="text")
                    else:
                        st.error(result["stderr"] or "Execution failed.")

prompt = st.chat_input("Ask anything, ask about your documents, or ask for code...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🌿 _Thinking..._")

        try:
            has_docs = st.session_state.rag_store.has_documents()

            if use_rag and has_docs:
                hits = st.session_state.rag_store.query(prompt)
                augmented_prompt = build_rag_prompt(prompt, hits)
                llm_messages = st.session_state.messages[:-1] + [
                    {"role": "user", "content": augmented_prompt}
                ]
                sources_note = ", ".join(sorted({h["source"] for h in hits})) if hits else None
            else:
                llm_messages = st.session_state.messages
                sources_note = None

            reply = chat_completion(llm_messages)

            if sources_note:
                reply += f"\n\n*Sources: {sources_note}*"

            placeholder.markdown(reply)

            code_blocks = extract_python_code_blocks(reply)
            for i, code in enumerate(code_blocks):
                if st.button(f"▶ Run code block {i + 1}", key=f"run_new_{i}"):
                    with st.spinner("Executing..."):
                        result = execute_python(code)
                    if result["success"]:
                        st.code(result["stdout"] or "(no output)", language="text")
                    else:
                        st.error(result["stderr"] or "Execution failed.")

            st.session_state.messages.append({"role": "assistant", "content": reply})

        except RuntimeError as e:
            placeholder.error(str(e))
        except Exception as e:
            placeholder.error(f"Something went wrong: {e}")
