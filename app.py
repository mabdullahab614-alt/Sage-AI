"""
Sage AI — Intelligent Document & Code Assistant
Built by Abdullah Javed.

Single-page Streamlit app: general chat + RAG over uploaded docs + code
gen/execution, with multiple saved chats (starrable + renameable), model
selection, an attach menu (photo / file / link), and per-message actions
(copy, regenerate, feedback).
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
    VISION_MODEL,
)
from utils.code_executor import execute_python
from utils.theme import inject_theme, render_empty_state, PAGE_TITLE, PAGE_ICON

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
inject_theme(st)

TITLE_MAX_LEN = 42
IMAGE_TYPES = ["png", "jpg", "jpeg", "gif", "webp"]
DOC_TYPES = ["pdf", "docx", "xlsx", "xls", "csv", "txt"]


# ---------- Conversation helpers ----------
def new_conversation() -> str:
    cid = str(uuid.uuid4())[:8]
    st.session_state.conversations[cid] = {"title": "New chat", "messages": [], "starred": False}
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
    """Copy button for an assistant message."""
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    copy_html = (
        '<div class="sage-msg-actions">'
        f'<button class="sage-action-btn" title="Copy" data-b64="{b64}" '
        "onclick=\""
        "const bytes = Uint8Array.from(atob(this.dataset.b64), c => c.charCodeAt(0));"
        "const text = new TextDecoder().decode(bytes);"
        "const btn = this;"
        "function fallbackCopy(t) {"
        "  const ta = document.createElement('textarea');"
        "  ta.value = t;"
        "  ta.style.position = 'fixed';"
        "  ta.style.left = '-9999px';"
        "  document.body.appendChild(ta);"
        "  ta.focus(); ta.select();"
        "  try { document.execCommand('copy'); } catch (e) {}"
        "  document.body.removeChild(ta);"
        "}"
        # Streamlit renders inside a sandboxed iframe, where
        # navigator.clipboard.writeText silently fails (no clipboard-write
        # permission granted to the frame) even though it looks like a
        # normal button click. That was the whole bug — the fallback
        # execCommand('copy') path below is what actually works there.
        "if (navigator.clipboard && navigator.clipboard.writeText) {"
        "  navigator.clipboard.writeText(text).then(() => {"
        "    btn.innerText = 'Copied'; setTimeout(() => btn.innerText = 'Copy', 1200);"
        "  }).catch(() => {"
        "    fallbackCopy(text);"
        "    btn.innerText = 'Copied'; setTimeout(() => btn.innerText = 'Copy', 1200);"
        "  });"
        "} else {"
        "  fallbackCopy(text);"
        "  btn.innerText = 'Copied'; setTimeout(() => btn.innerText = 'Copy', 1200);"
        "}"
        "\">Copy</button>"
        "</div>"
    )
    st.markdown(copy_html, unsafe_allow_html=True)


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
if "renaming_id" not in st.session_state:
    st.session_state.renaming_id = None
if "pending_files" not in st.session_state:
    st.session_state.pending_files = []          # list of UploadedFile objects, queued via "+"
if "pending_links" not in st.session_state:
    st.session_state.pending_links = []           # list of url strings, queued via "+"
if "uploader_version" not in st.session_state:
    # Bumping this changes the file_uploader widget keys below, forcing
    # Streamlit to give us a fresh (empty) uploader instead of one that
    # still remembers the previously-selected files. Without this,
    # clearing pending_files alone does nothing because the uploader
    # widget itself keeps re-feeding the same files back in on rerun.
    st.session_state.uploader_version = 0
if "use_rag_toggle" not in st.session_state:
    st.session_state.use_rag_toggle = bool(st.session_state.uploaded_filenames)
if "rag_auto_synced" not in st.session_state:
    # Chroma's persistent store can already contain documents from an
    # earlier session (page reload, etc.) even though uploaded_filenames
    # (a plain session list) has reset to empty. Catch that case once per
    # session so the toggle reflects reality instead of defaulting off.
    if st.session_state.rag_store.has_documents():
        st.session_state.use_rag_toggle = True
    st.session_state.rag_auto_synced = True

# Backfill "starred" on conversations created before this feature existed.
for _conv in st.session_state.conversations.values():
    _conv.setdefault("starred", False)

current_conv = st.session_state.conversations[st.session_state.current_id]
messages = current_conv["messages"]


def _reset_pending_attachments() -> None:
    """Clears queued attachments AND resets the uploader widgets so they
    don't silently re-populate pending_files with the same files again."""
    st.session_state.pending_files = []
    st.session_state.pending_links = []
    st.session_state.uploader_version += 1


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

    # Most-recent-first.
    chat_items = list(st.session_state.conversations.items())[::-1]

    for cid, conv in chat_items:
        if st.session_state.renaming_id == cid:
            # ---- Rename mode: text input + save/cancel ----
            new_title = st.text_input(
                "Rename chat", value=conv["title"], key=f"rename_input_{cid}",
                label_visibility="collapsed",
            )
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("Save", key=f"save_{cid}", use_container_width=True):
                    conv["title"] = new_title.strip() or "New chat"
                    st.session_state.renaming_id = None
                    st.rerun()
            with rc2:
                if st.button("Cancel", key=f"cancel_{cid}", use_container_width=True):
                    st.session_state.renaming_id = None
                    st.rerun()
        else:
            is_active = cid == st.session_state.current_id
            c_title, c_rename, c_del = st.columns([4, 0.8, 0.8])
            with c_title:
                if st.button(
                    conv["title"] or "New chat",
                    key=f"switch_{cid}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.current_id = cid
                    st.rerun()
            with c_rename:
                st.markdown('<div class="sage-chatrow-icon">', unsafe_allow_html=True)
                if st.button("✎", key=f"ren_{cid}", help="Rename this chat", use_container_width=True):
                    st.session_state.renaming_id = cid
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_del:
                st.markdown('<div class="sage-chatrow-icon">', unsafe_allow_html=True)
                if st.button("×", key=f"del_{cid}", help="Delete this chat", use_container_width=True):
                    del st.session_state.conversations[cid]
                    if not st.session_state.conversations:
                        new_conversation()
                    elif st.session_state.current_id == cid:
                        st.session_state.current_id = next(iter(st.session_state.conversations))
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    if st.session_state.uploaded_filenames:
        st.markdown('<p class="sage-eyebrow">Indexed documents</p>', unsafe_allow_html=True)
        for fn in st.session_state.uploaded_filenames:
            st.markdown(f"📄 {fn}")
        if st.button("Clear documents", use_container_width=True):
            st.session_state.rag_store.clear()
            st.session_state.uploaded_filenames = []
            st.rerun()

    st.divider()
    st.toggle(
        "Ground answers in documents",
        key="use_rag_toggle",
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


def _image_to_data_url(uf) -> str:
    """Encodes an uploaded image file as a base64 data: URL for Groq's
    multimodal (vision) message format."""
    ext = uf.name.lower().rsplit(".", 1)[-1]
    mime = "image/jpeg" if ext == "jpg" else f"image/{ext}"
    b64 = base64.b64encode(uf.getvalue()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _index_uploaded_file(uf) -> None:
    """Parses + indexes one uploaded file into the RAG store."""
    if uf.name in st.session_state.uploaded_filenames:
        # Already indexed earlier in this session — still make sure RAG
        # grounding is on for this turn, since this is exactly the case
        # that was silently skipping the toggle-on step before.
        st.session_state.use_rag_toggle = True
        return
    try:
        with st.spinner(f"Reading {uf.name}..."):
            parsed = parse_document(uf)
            num_chunks = st.session_state.rag_store.add_document(parsed["filename"], parsed["text"])
        st.session_state.uploaded_filenames.append(uf.name)
        # A document just got indexed this turn — make sure RAG grounding
        # is actually switched on for the reply we're about to generate,
        # instead of relying on a toggle value that was read before this
        # file existed.
        st.session_state.use_rag_toggle = True
        st.toast(f"{uf.name} indexed — {num_chunks} chunks ready")
    except UnsupportedFileTypeError as e:
        st.error(str(e))
    except EmptyDocumentError as e:
        st.warning(str(e))
    except Exception as e:
        st.error(f"Couldn't process {uf.name}: {e}")


# ---------- Toolbar row: attach ("+") + model + voice ----------
# Streamlit's native chat_input "+" only opens a raw file dialog — it can't
# show a menu. This custom "+" popover replaces that: it opens a real menu
# with Photo / File / Link tabs, queues what you pick as chips above the
# input, and everything gets attached when you hit send. accept_file is
# turned off on chat_input below so there's only ONE attach control, not two.
toolbar_col1, toolbar_col2, toolbar_col3, toolbar_spacer = st.columns([0.07, 0.07, 0.07, 0.79])

uv = st.session_state.uploader_version  # current uploader "generation"

with toolbar_col1:
    with st.popover("＋", use_container_width=True):
        st.caption("Add to this message")
        tab_photo, tab_file, tab_link = st.tabs(["📷 Photo", "📄 File", "🔗 Link"])

        with tab_photo:
            photos = st.file_uploader(
                "Upload photos", type=IMAGE_TYPES, accept_multiple_files=True,
                label_visibility="collapsed", key=f"attach_photo_uploader_{uv}",
            )
            if photos:
                existing = {f.name for f in st.session_state.pending_files}
                for p in photos:
                    if p.name not in existing:
                        st.session_state.pending_files.append(p)

        with tab_file:
            docs = st.file_uploader(
                "Upload files", type=DOC_TYPES, accept_multiple_files=True,
                label_visibility="collapsed", key=f"attach_file_uploader_{uv}",
            )
            if docs:
                existing = {f.name for f in st.session_state.pending_files}
                for d in docs:
                    if d.name not in existing:
                        st.session_state.pending_files.append(d)

        with tab_link:
            link_val = st.text_input("Paste a link", key="attach_link_input", label_visibility="collapsed")
            if st.button("Add link", key="add_link_btn"):
                cleaned = link_val.strip()
                if cleaned and cleaned not in st.session_state.pending_links:
                    st.session_state.pending_links.append(cleaned)
                    st.rerun()

with toolbar_col2:
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

with toolbar_col3:
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

# ---------- Pending attachment chips ----------
if st.session_state.pending_files or st.session_state.pending_links:
    chip_html = ['<div class="sage-chip-row">']
    for pf in st.session_state.pending_files:
        chip_html.append(f'<span class="sage-chip">📎 {pf.name}</span>')
    for pl in st.session_state.pending_links:
        chip_html.append(f'<span class="sage-chip">🔗 {pl}</span>')
    chip_html.append("</div>")
    st.markdown("".join(chip_html), unsafe_allow_html=True)
    if st.button("Clear attachments", key="clear_pending"):
        _reset_pending_attachments()
        st.rerun()

chat_value = st.chat_input(
    "Ask anything, ask about your documents, or ask for code...",
    accept_file=False,  # replaced by the custom "+" attach menu above
)
# NOTE: with accept_file=False, chat_input returns a plain str (or None) —
# not the ChatInputValue object you get with accept_file="multiple"/True.
# That mismatch (treating it like an object with .text) was the AttributeError.
if chat_value:
    typed_prompt = chat_value.strip()
    if typed_prompt:
        prompt = typed_prompt

if prompt:
    # Fold in anything queued via the "+" menu. Images and documents are
    # handled differently: documents get chunked into the RAG store,
    # images get sent straight to the vision model as part of this turn.
    image_files = [
        pf for pf in st.session_state.pending_files
        if pf.name.lower().rsplit(".", 1)[-1] in IMAGE_TYPES
    ]
    doc_files = [pf for pf in st.session_state.pending_files if pf not in image_files]

    for pf in doc_files:
        _index_uploaded_file(pf)

    if st.session_state.pending_links:
        links_note = "\n".join(f"🔗 {u}" for u in st.session_state.pending_links)
        prompt = f"{prompt}\n\n{links_note}"
    _reset_pending_attachments()

    messages.append({"role": "user", "content": prompt})
    if current_conv["title"] == "New chat":
        current_conv["title"] = prompt[:TITLE_MAX_LEN] + ("…" if len(prompt) > TITLE_MAX_LEN else "")

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🌿 _Thinking..._")

        try:
            model_for_this_turn = st.session_state.selected_model
            sources_note = None

            if image_files:
                # Vision turn: build a multimodal message (text + one or
                # more images) and force the vision-capable model, since
                # none of the plain text models in AVAILABLE_MODELS can
                # actually read image content.
                content_parts = [{"type": "text", "text": prompt}]
                for img in image_files:
                    content_parts.append(
                        {"type": "image_url", "image_url": {"url": _image_to_data_url(img)}}
                    )
                llm_messages = messages[:-1] + [{"role": "user", "content": content_parts}]
                model_for_this_turn = VISION_MODEL
            else:
                has_docs = st.session_state.rag_store.has_documents()
                # Re-read the toggle here (not the stale sidebar-render-time
                # value) so a file indexed earlier in THIS same run is honored.
                use_rag = st.session_state.use_rag_toggle

                if use_rag and has_docs:
                    hits = st.session_state.rag_store.query(prompt)
                    augmented_prompt = build_rag_prompt(prompt, hits)
                    llm_messages = messages[:-1] + [{"role": "user", "content": augmented_prompt}]
                    sources_note = ", ".join(sorted({h["source"] for h in hits})) if hits else None
                else:
                    llm_messages = messages

            reply = chat_completion(llm_messages, model=model_for_this_turn)

            if sources_note:
                reply += f"\n\n*Sources: {sources_note}*"

            placeholder.markdown(reply)
            messages.append({"role": "assistant", "content": reply})
            st.rerun()  # re-render through the message loop so copy/like/regenerate/run-code show up

        except RuntimeError as e:
            placeholder.error(str(e))
        except Exception as e:
            placeholder.error(f"Something went wrong: {e}")
