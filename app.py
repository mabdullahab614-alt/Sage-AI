"""
Sage AI — Intelligent Document & Code Assistant
Built by Abdullah Javed.

Single-page Streamlit app: general chat + RAG over uploaded docs + code
gen/execution, with multiple saved chats, model selection, and per-message
actions (copy, regenerate, feedback).
"""

import base64
import hashlib
import uuid

import streamlit as st

from utils.document_parser import parse_document, UnsupportedFileTypeError, EmptyDocumentError
from utils.rag import RAGStore, build_rag_prompt
from utils.llm import (
    chat_completion,
    extract_python_code_blocks,
    transcribe_audio,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
)
from utils.code_executor import execute_python
from utils.theme import inject_theme, render_empty_state, PAGE_TITLE, PAGE_ICON

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
inject_theme(st)

TITLE_MAX_LEN = 42


# ---------- Conversation helpers ----------
def new_conversation() -> str:
    cid = str(uuid.uuid4())[:8]
    st.session_state.conversations[cid] = {"title": "New chat", "messages": []}
    st.session_state.current_id = cid
    return cid


def conversation_to_markdown(conv: dict) -> str:
    lines = [f"# {conv['title']}", ""]
    for m in conv["messages"]:
        speaker = "You" if m["role"] == "user" else "Sage"
        lines.append(f"**{speaker}:**\n\n{m['content']}\n")
    return "\n".join(lines)


def regenerate_last_response(conv_id: str) -> None:
    """Drops the last assistant reply in a conversation and re-generates it."""
    conv = st.session_state.conversations[conv_id]
    if conv["messages"] and conv["messages"][-1]["role"] == "assistant":
        conv["messages"].pop()
    if not conv["messages"] or conv["messages"][-1]["role"] != "user":
        return
    try:
        with st.spinner("Regenerating..."):
            reply = chat_completion(conv["messages"], model=st.session_state.selected_model)
        conv["messages"].append({"role": "assistant", "content": reply})
    except Exception as e:
        conv["messages"].append({"role": "assistant", "content": f"Something went wrong: {e}"})


def render_message_actions(conv_id: str, idx: int, content: str, is_last: bool) -> None:
    """Copy / thumbs up / thumbs down / regenerate (last message only) row."""
    fb_key = (conv_id, idx)
    current_fb = st.session_state.feedback.get(fb_key)

    cols = st.columns(4) if is_last else st.columns(3)

    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    copy_html = (
        f'<button class="sage-action-btn" title="Copy" data-b64="{b64}" '
        f"onclick=\"const bytes=Uint8Array.from(atob(this.dataset.b64),c=>c.charCodeAt(0)); "
        f"navigator.clipboard.writeText(new TextDecoder().decode(bytes)); "
        f"this.innerText='Copied'; setTimeout(()=&gt;this.innerText='Copy',1200);\">Copy</button>"
    )
    with cols[0]:
        st.markdown(copy_html, unsafe_allow_html=True)
    with cols[1]:
        label = "Liked" if current_fb == "up" else "Like"
        if st.button(label, key=f"up_{conv_id}_{idx}"):
            st.session_state.feedback[fb_key] = "up"
            st.toast("Thanks for the feedback.")
            st.rerun()
    with cols[2]:
        label = "Disliked" if current_fb == "down" else "Dislike"
        if st.button(label, key=f"down_{conv_id}_{idx}"):
            st.session_state.feedback[fb_key] = "down"
            st.toast("Thanks — noted.")
            st.rerun()
    if is_last:
        with cols[3]:
            if st.button("Regenerate", key=f"regen_{conv_id}_{idx}"):
                regenerate_last_response(conv_id)
                st.rerun()


def render_code_run_buttons(code_blocks: list[str], key_prefix: str) -> None:
    for j, code in enumerate(code_blocks):
        if st.button(f"▶ Run code block {j + 1}", key=f"{key_prefix}_{j}"):
            with st.spinner("Executing..."):
                result = execute_python(code)
            if result["success"]:
                st.code(result["stdout"] or "(no output)", language="text")
            else:
                st.error(result["stderr"] or "Execution failed.")


# ---------- Session state ----------
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.current_id = None
if not st.session_state.conversations:
    new_conversation()
elif st.session_state.current_id not in st.session_state.conversations:
    st.session_state.current_id = next(iter(st.session_state.conversations))

if "rag_store" not in st.session_state:
    st.session_state.rag_store = RAGStore()
if "uploaded_filenames" not in st.session_state:
    st.session_state.uploaded_filenames = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}
if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

current_conv = st.session_state.conversations[st.session_state.current_id]
messages = current_conv["messages"]


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        '<h3><span class="sage-leaf-icon">🌿</span> Sage AI</h3>',
        unsafe_allow_html=True,
    )
    st.write("")

    if st.button("+ New chat", use_container_width=True):
        new_conversation()
        st.rerun()

    st.markdown('<p class="sage-eyebrow">Chats</p>', unsafe_allow_html=True)
    for cid, conv in list(st.session_state.conversations.items())[::-1]:
        is_active = cid == st.session_state.current_id
        c1, c2 = st.columns([5, 1])
        with c1:
            if st.button(
                conv["title"] or "New chat",
                key=f"switch_{cid}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.current_id = cid
                st.rerun()
        with c2:
            if st.button("×", key=f"del_{cid}", help="Delete this chat"):
                del st.session_state.conversations[cid]
                if not st.session_state.conversations:
                    new_conversation()
                elif st.session_state.current_id == cid:
                    st.session_state.current_id = next(iter(st.session_state.conversations))
                st.rerun()

    st.divider()

    # Model picker and document upload used to live here — both moved down
    # to the control row right above the chat box (see bottom of file),
    # next to the "+" attach button and mic, so everything needed to send
    # a message lives in one place instead of being split across the page.
    # The indexed-files list and "Clear documents" stay here since this is
    # a status/management view, not an input control.
    if st.session_state.uploaded_filenames:
        st.markdown('<p class="sage-eyebrow">Indexed documents</p>', unsafe_allow_html=True)
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
        help="When on, questions are answered using retrieved document context. "
             "Documents you upload are shared across all your chats.",
    )

    st.divider()
    if messages:
        st.download_button(
            "Export this chat",
            data=conversation_to_markdown(current_conv),
            file_name=f"{(current_conv['title'] or 'sage-chat')[:40]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button("Clear conversation", use_container_width=True):
        current_conv["messages"] = []
        current_conv["title"] = "New chat"
        st.rerun()


# ---------- Main chat area ----------
if not messages:
    render_empty_state(st)

for i, msg in enumerate(messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_message_actions(
                st.session_state.current_id, i, msg["content"], is_last=(i == len(messages) - 1)
            )
            code_blocks = extract_python_code_blocks(msg["content"])
            render_code_run_buttons(code_blocks, key_prefix=f"run_{st.session_state.current_id}_{i}")

prompt = None


def _index_uploaded_file(uf) -> None:
    """Parses + indexes one uploaded file into the RAG store, same logic
    that used to live in the sidebar's file_uploader handler."""
    if uf.name in st.session_state.uploaded_filenames:
        return
    try:
        with st.spinner(f"Reading {uf.name}..."):
            parsed = parse_document(uf)
            num_chunks = st.session_state.rag_store.add_document(parsed["filename"], parsed["text"])
        st.session_state.uploaded_filenames.append(uf.name)
        st.toast(f"{uf.name} indexed — {num_chunks} chunks ready")
    except UnsupportedFileTypeError as e:
        st.error(str(e))
    except EmptyDocumentError as e:
        st.warning(str(e))
    except Exception as e:
        st.error(f"Couldn't process {uf.name}: {e}")


# ---------- Compact control row (model + voice), docked right above the
# chat box — this plus the box's own built-in "+" attach button below is
# the closest a pure-Streamlit chat_input can get to a single fused input
# bar like Claude's. It's two adjacent, CSS-matched elements rather than
# one literal HTML control (Streamlit's chat_input doesn't support
# embedding arbitrary widgets inside it), but it reads as one unit and
# everything needed to send a message now lives in this one spot instead
# of being split off in the sidebar. ----------
with st.container(key="sage_inputbar_wrapper"):
    with st.container(key="sage_ctrl_model"):
        model_labels = list(AVAILABLE_MODELS.keys())
        current_label = next(
            (label for label, mid in AVAILABLE_MODELS.items() if mid == st.session_state.selected_model),
            model_labels[0],
        )
        with st.popover("⚙️", use_container_width=True):
            st.caption("Model")
            chosen_label = st.selectbox(
                "Model", model_labels, index=model_labels.index(current_label),
                label_visibility="collapsed", key="model_picker",
            )
            st.session_state.selected_model = AVAILABLE_MODELS[chosen_label]

    with st.container(key="sage_ctrl_mic"):
        with st.popover("🎤", use_container_width=True):
            st.caption("Record a voice message")
            audio_value = st.audio_input("Record a voice message", label_visibility="collapsed")
            if audio_value is not None:
                audio_bytes = audio_value.getvalue()
                audio_hash = hashlib.md5(audio_bytes).hexdigest()
                if audio_hash != st.session_state.last_audio_hash:
                    st.session_state.last_audio_hash = audio_hash
                    try:
                        with st.spinner("Transcribing your voice message..."):
                            transcribed = transcribe_audio(
                                audio_bytes, filename=getattr(audio_value, "name", "voice.wav")
                            )
                        transcribed = (transcribed or "").strip()
                        if transcribed:
                            prompt = transcribed
                        else:
                            st.warning("Didn't catch any speech in that recording — try again.")
                    except RuntimeError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Transcription failed: {e}")

    chat_value = st.chat_input(
        "Ask anything, ask about your documents, or ask for code...",
        accept_file="multiple",
        file_type=["pdf", "docx", "xlsx", "xls", "csv", "txt"],
    )

if chat_value:
    for uf in chat_value.files or []:
        _index_uploaded_file(uf)
    typed_prompt = (chat_value.text or "").strip()
    if typed_prompt:
        prompt = typed_prompt

if prompt:
    messages.append({"role": "user", "content": prompt})
    if current_conv["title"] == "New chat":
        current_conv["title"] = prompt[:TITLE_MAX_LEN] + ("…" if len(prompt) > TITLE_MAX_LEN else "")

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
                llm_messages = messages[:-1] + [{"role": "user", "content": augmented_prompt}]
                sources_note = ", ".join(sorted({h["source"] for h in hits})) if hits else None
            else:
                llm_messages = messages
                sources_note = None

            reply = chat_completion(llm_messages, model=st.session_state.selected_model)

            if sources_note:
                reply += f"\n\n*Sources: {sources_note}*"

            placeholder.markdown(reply)
            messages.append({"role": "assistant", "content": reply})
            st.rerun()  # re-render through the message loop so copy/like/regenerate/run-code show up

        except RuntimeError as e:
            placeholder.error(str(e))
        except Exception as e:
            placeholder.error(f"Something went wrong: {e}")
