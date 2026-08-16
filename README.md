<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:14181a,40:1b211c,100:5c7a4e&height=200&section=header&text=Sage%20AI&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Intelligent%20Document%20and%20Code%20Assistant&descAlignY=58&descSize=16&descColor=d9e6cf" width="100%" alt="Sage AI banner"/>

<br/>

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=20&pause=1200&color=8FAE7C&center=true&vCenter=true&width=640&lines=Chat+%2B+RAG+over+your+documents;Generate+and+run+Python+code+live;Multiple+saved%2C+renameable+chats;Voice+input%2C+vision%2C+one-click+export" alt="Typing SVG"/>

<br/><br/>

<img src="https://img.shields.io/badge/Built%20With-Streamlit%20%7C%20Python-FF4B4B?style=for-the-badge&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/LLM-Groq-F55036?style=for-the-badge&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/Vector%20Store-ChromaDB-8FAE7C?style=for-the-badge&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/Hosted%20On-Streamlit%20Cloud-D9A94E?style=for-the-badge&labelColor=14181a"/>

<br/><br/>

<img src="https://img.shields.io/github/last-commit/mabdullahab614-alt/Sage-AI?style=flat-square&color=8fae7c&labelColor=14181a&label=Last%20Updated"/>
&nbsp;
<img src="https://img.shields.io/github/languages/top/mabdullahab614-alt/Sage-AI?style=flat-square&color=D9A94E&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/github/repo-size/mabdullahab614-alt/Sage-AI?style=flat-square&color=5C7A4E&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/License-All%20Rights%20Reserved-E2725B?style=flat-square&labelColor=14181a"/>

<br/><br/>

<a href="https://sage-ai-q9bvrp6nmajtrxp9rp9zna.streamlit.app/">
  <img src="https://capsule-render.vercel.app/api?type=rounded&color=0:8fae7c,100:14181a&height=85&section=header&text=TRY%20IT%20LIVE&fontSize=32&fontColor=ffffff&animation=twinkling&fontAlignY=62&width=420" alt="Try Sage AI live"/>
</a>
&nbsp;
<a href="#-run-locally">
  <img src="https://capsule-render.vercel.app/api?type=rounded&color=0:1b211c,100:14181a&height=85&section=header&text=RUN%20LOCALLY&fontSize=32&fontColor=d9a94e&animation=twinkling&fontAlignY=62&width=420" alt="Run locally"/>
</a>

</div>

<br/>

<!--
SEO: AI document assistant, RAG chatbot Streamlit, chat with PDF Word Excel CSV, Groq LLM
chatbot, Python code generator and executor, free AI assistant, ChromaDB RAG app, voice to
text AI assistant, GPT-OSS chatbot, open source AI chat app.
-->

<div align="center">

## 📌 Table of Contents

</div>

<table align="center">
<tr>
<td valign="top">

🎯 [What It Does](#-what-it-does)
🧩 [Features](#-features)
🧠 [Models](#-models)

</td>
<td valign="top">

🛠️ [Tech Stack](#️-tech-stack)
📂 [Folder Structure](#-folder-structure)
🚀 [Run Locally](#-run-locally)

</td>
<td valign="top">

🔒 [Security Notes](#-security-notes)
🎨 [Design System](#-design-system)
📄 [License](#-license)

</td>
</tr>
</table>

<br/>

---

<br/>

## 🎯 What It Does

- 🌿 A single-page Streamlit AI assistant — chat, document Q&A, and live code execution in one app
- 💬 General chat, powered by fast open models on **Groq**
- 📄 **RAG over your own documents** — upload PDF/DOCX/XLSX/CSV/TXT, ask questions grounded in them
- 🐍 Generates Python code and **runs it live**, right inside the chat
- 🗂️ Multiple saved, renameable chats — switch, rename, or delete anytime
- 🎙️ Voice input — record a message, it's transcribed automatically
- 🖼️ Vision — attach a photo and ask about it
- 📤 Export any chat to a Markdown file
- 🔐 100% free stack — no paid API required beyond a free Groq key

<br/>

---

<br/>

## 🧩 Features

<div align="center">

| | | |
|:--:|:--:|:--:|
| 💬 **Multi-chat sidebar**<br/>New chat, rename, delete, auto-titled from first message | 📎 **Attach menu**<br/>Photo / File / Link — all in one popover | ⚙️ **Model picker**<br/>Switch between 3 Groq models mid-conversation |
| 📄 **Document RAG**<br/>PDF, DOCX, XLSX/XLS, CSV, TXT — indexed and queryable | 🎙️ **Voice input**<br/>Record → transcribed via Whisper-large-v3-turbo | 🖼️ **Vision**<br/>Attach an image, ask questions about it |
| ▶️ **Run code inline**<br/>Every Python block gets a "Run" button with live output | 📋 **Copy responses**<br/>One-click copy with a clipboard fallback | 🔁 **Regenerate**<br/>Re-run the last response with the current model |
| 📤 **Export chat**<br/>Download any conversation as a `.md` file | 🧭 **Sources shown**<br/>RAG answers cite which document they came from | ♿ **Reduced motion**<br/>All animations respect `prefers-reduced-motion` |

</div>

<br/>

---

<br/>

## 🧠 Models

<div align="center">

| Model | Via Groq | Role |
|:--|:--|:--|
| **GPT-OSS 120B** | `openai/gpt-oss-120b` | Default — best all-round quality |
| **GPT-OSS 20B** | `openai/gpt-oss-20b` | Fastest responses |
| **Qwen 3.6 27B** | `qwen/qwen3.6-27b` | Flagship reasoning + coding |
| **Qwen 3.6 27B** *(vision)* | `qwen/qwen3.6-27b` | Auto-selected for image attachments |
| **Whisper Large v3 Turbo** | `whisper-large-v3-turbo` | Voice message transcription |

</div>

> ⚠️ `llama-3.3-70b-versatile` and `llama-3.1-8b-instant` were deprecated by Groq and shut down — they're deliberately excluded from the model list rather than left in as a broken option.

<br/>

---

<br/>

## 🛠️ Tech Stack

<div align="center">

<img src="https://img.shields.io/badge/Streamlit-1.61.1-FF4B4B?style=flat-square&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/Groq%20SDK-1.6.0-F55036?style=flat-square&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/ChromaDB-1.5.9-8FAE7C?style=flat-square&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/pandas-2.2.3-150458?style=flat-square&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/pypdf-5.1.0-D9A94E?style=flat-square&labelColor=14181a"/>
&nbsp;
<img src="https://img.shields.io/badge/python--docx-1.1.2-2B579A?style=flat-square&labelColor=14181a"/>

</div>

- 🖥️ **Streamlit** — the entire UI, no separate frontend framework
- 🧠 **Groq** — LLM inference (chat + vision) and Whisper transcription
- 🗄️ **ChromaDB** — local vector store for RAG, using its built-in **ONNX** embedding function
- ✂️ **LangChain Text Splitters** — `RecursiveCharacterTextSplitter` for chunking (800 chars, 150 overlap)
- 📄 **pypdf / python-docx / pandas + openpyxl** — parsing PDF / DOCX / XLSX / CSV respectively

> 💡 **Why ONNX instead of `sentence-transformers`?** The torch + transformers stack is heavy enough to exceed Streamlit Community Cloud's free-tier build resources. ChromaDB's `DefaultEmbeddingFunction` uses the same underlying MiniLM architecture via ONNX runtime — functionally similar, at a fraction of the install footprint.

<br/>

---

<br/>

## 📂 Folder Structure

```
Sage-AI/
│
├── 📄 app.py                     → main Streamlit app — UI, chat state, message flow
│
├── 📁 utils/
│   ├── 🧠 llm.py                   → Groq wrapper — chat, vision, transcription, model list
│   ├── 📄 document_parser.py        → PDF / DOCX / XLSX / CSV / TXT → plain text
│   ├── 🔍 rag.py                     → ChromaDB store — chunk, embed, retrieve
│   ├── ▶️ code_executor.py            → sandboxed Python execution
│   └── 🎨 theme.py                     → custom CSS, fonts, SEO meta injection
│
├── 📦 requirements.txt            → pinned dependencies
├── ⚙️ runtime.txt                  → Python runtime version
└── 🙈 .gitignore
```

<br/>

---

<br/>

## 🚀 Run Locally

```bash
git clone https://github.com/mabdullahab614-alt/Sage-AI.git
cd Sage-AI
pip install -r requirements.txt
```

- 🔑 Get a **free Groq API key** → [console.groq.com/keys](https://console.groq.com/keys)
- 🔐 Set it as an environment variable:

```bash
export GROQ_API_KEY="your-key-here"      # macOS/Linux
setx GROQ_API_KEY "your-key-here"        # Windows
```

- ▶️ Run the app:

```bash
streamlit run app.py
```

- 🌐 Opens at [http://localhost:8501](http://localhost:8501)

<br/>

---

<br/>

## 🔒 Security Notes

- ⚠️ Code execution runs in a **subprocess with resource limits** (CPU time, 256MB memory cap, 10s timeout, 32-process cap) — a best-effort MVP sandbox, **not a hard security boundary**
- 🧱 For a real production deployment, swap the executor for a proper isolated sandbox — [E2B](https://e2b.dev) or [Judge0](https://judge0.com) both have free tiers and actually isolate execution in a separate container/VM
- 🔑 `GROQ_API_KEY` is read from environment variables only — never hardcoded, never committed

<br/>

---

<br/>

## 🎨 Design System

- 🌿 **Sage green** — the literal plant color the brand is named after (wisdom, calm, growth)
- 🖤 **Warm charcoal** background — depth without a flat "pure black" look
- 🟡 **Warm gold** — confidence/warmth accent for primary actions
- 🔤 **Fraunces** (display/headers) + **Plus Jakarta Sans** (body) + **JetBrains Mono** (code)
- 🍃 A signature breathing leaf mark next to the wordmark — everything else stays disciplined
- ✨ Gradient shimmer on the empty-state greeting, subtle button-vibrate on hover, animated input glow
- 🔍 SEO meta tags (title, description, Open Graph, Twitter Card) injected at runtime
- ♿ Every animation backs off automatically for `prefers-reduced-motion`

<br/>

---

<br/>

## 📄 License

🔒 **ALL RIGHTS RESERVED**

**All Rights Reserved © 2026 Abdullah Javed**

- 👀 Repository is publicly visible for **portfolio and demonstration purposes only**
- 🚫 No copying, modifying, distributing, sublicensing, or reuse — in whole or in part — without explicit written permission
- 🚫 Forking or cloning does **not** grant any usage rights

<br/>

<div align="center">

📧 [mabdullah.ab614@gmail.com](mailto:mabdullah.ab614@gmail.com)
&nbsp;|&nbsp;
🔗 [github.com/mabdullahab614-alt](https://github.com/mabdullahab614-alt)
&nbsp;|&nbsp;
💼 [linkedin.com/in/abdullah-javid-b217a2384](https://linkedin.com/in/abdullah-javid-b217a2384)

<br/><br/>

`#SageAI` `#Streamlit` `#Groq` `#RAG` `#ChromaDB` `#Python` `#AIAssistant` `#AISeekho`

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:5c7a4e,60:1b211c,100:14181a&height=110&section=footer" width="100%" alt="footer banner"/>

<i>🌿 Sage AI — built by Abdullah Javed</i>

</div>
