"""
Sage AI — visual theme.

Design language: "a naturalist's field notebook, drafted like a blueprint."
Deep cyanotype blue instead of the usual near-black chat-app dark mode. A
single hand-drawn line-art leaf diagram (no emoji) stands in for the brand
mark, echoed as a faint watermark. Cards are framed like technical-drawing
callouts with corner registration marks. The footer is built as an actual
engineering title block — labelled cells, not a generic link list.

Usage (top of app.py, right after st.set_page_config):

    from utils.theme import inject_theme, render_header, render_hero, render_footer

    inject_theme()
    render_header()
    ... existing app body ...
    render_footer()
"""

import streamlit as st

GITHUB_URL = "https://github.com/mabdullahab614-alt/Sage-AI"
LIVE_URL = "https://sage-ai-q9bvrp6nmajtrxp9rp9zna.streamlit.app"
AUTHOR = "Abdullah Javed"

# A drawn botanical line diagram — center vein + side veins, stroke only.
# Reused everywhere instead of an emoji leaf.
LEAF_SVG = """
<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="sg-leaf-svg">
  <path d="M16 3.5C9.6 7.4 5.6 13.8 5.6 19.6c0 5.1 4.6 8.9 10.4 8.9s10.4-3.8 10.4-8.9C26.4 13.8 22.4 7.4 16 3.5z"
        stroke="currentColor" stroke-width="1.3"/>
  <path d="M16 6.5v20.5" stroke="currentColor" stroke-width=".9"/>
  <path d="M16 11.5l-4.6 2.8M16 11.5l4.6 2.8M16 17.5l-4 2.4M16 17.5l4 2.4M16 23l-3 1.9M16 23l3 1.9"
        stroke="currentColor" stroke-width=".7"/>
</svg>
"""

_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root{
  --bg:            #0f2334;
  --bg-raised:     #163149;
  --bg-raised-2:   #1c3c58;
  --ink:           #eef1e8;
  --ink-muted:     #93a9b6;
  --ink-faint:     #5d7383;
  --brass:         #c88a34;
  --brass-bright:  #e2a950;
  --line:          rgba(238,241,232,0.10);
  --line-strong:   rgba(238,241,232,0.24);
  --shadow-1:      0 1px 2px rgba(0,0,0,.35);
  --shadow-2:      0 10px 26px rgba(0,0,0,.38);
  --ease:          cubic-bezier(.2,.75,.3,1);
}

@media (prefers-reduced-motion: reduce){
  *{ animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }
}

html, body, [class*="css"]{ font-family: 'IBM Plex Sans', sans-serif; }

.stApp{
  background-color: var(--bg);
  background-image:
    linear-gradient(var(--line) 1px, transparent 1px),
    linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size: 34px 34px;
  color: var(--ink);
}

section[data-testid="stSidebar"]{
  background: var(--bg-raised);
  border-right: 1px solid var(--line-strong);
}
section[data-testid="stSidebar"] *{ color: var(--ink); }

.block-container{ padding-top: 1rem; max-width: 960px; }

::-webkit-scrollbar{ width: 9px; height: 9px; }
::-webkit-scrollbar-track{ background: var(--bg); }
::-webkit-scrollbar-thumb{ background: var(--bg-raised-2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover{ background: var(--brass); }
:focus-visible{ outline: 1.5px solid var(--brass-bright); outline-offset: 2px; }

.sg-leaf-svg{ width: 100%; height: 100%; color: var(--brass-bright); display: block; }

@keyframes floatIn{ from{ opacity:0; transform: translateY(-6px);} to{ opacity:1; transform: translateY(0);} }
@keyframes fadeUp{ from{ opacity:0; transform: translateY(8px);} to{ opacity:1; transform: translateY(0);} }
@keyframes blink{ 0%,49%{ opacity:1;} 50%,100%{ opacity:0;} }
@keyframes sway{ 0%,100%{ transform: rotate(-3deg);} 50%{ transform: rotate(3deg);} }

/* ---------------------------------------------------------------- */
/* Corner-bracket frame — the shared "technical drawing" motif       */
/* ---------------------------------------------------------------- */
.sg-frame{ position: relative; }
.sg-frame::before, .sg-frame::after{
  content: ""; position: absolute; width: 12px; height: 12px;
  border: 1.5px solid var(--brass); opacity: .8; transition: width .25s var(--ease), height .25s var(--ease);
}
.sg-frame::before{ top: -1px; left: -1px; border-right: none; border-bottom: none; }
.sg-frame::after{ bottom: -1px; right: -1px; border-left: none; border-top: none; }
.sg-frame:hover::before, .sg-frame:hover::after{ width: 18px; height: 18px; }

/* ---------------------------------------------------------------- */
/* Header — instrument panel, not a glass navbar                     */
/* ---------------------------------------------------------------- */
.sg-header{
  position: sticky; top: 0; z-index: 999;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
  margin: -1rem -1rem 1.6rem -1rem;
  padding: .9rem 1.5rem;
  background: rgba(15,35,52,.72);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line-strong);
  animation: floatIn .5s var(--ease);
}
.sg-brand{ display: flex; align-items: center; gap: .8rem; }
.sg-brand-mark{
  width: 34px; height: 34px; padding: 6px; border: 1px solid var(--line-strong); border-radius: 3px;
  animation: sway 6s ease-in-out infinite; transform-origin: 50% 90%;
}
.sg-word{
  font-family: 'Newsreader', serif; font-weight: 600; font-size: 1.3rem;
  letter-spacing: .04em; text-transform: uppercase; color: var(--ink); line-height: 1;
}
.sg-tag{
  font-family: 'IBM Plex Mono', monospace; font-size: .66rem; color: var(--ink-faint);
  letter-spacing: .08em; text-transform: uppercase; margin-top: 3px;
}
.sg-status{
  font-family: 'IBM Plex Mono', monospace; font-size: .68rem; letter-spacing: .04em;
  color: var(--ink-muted); border: 1px solid var(--line-strong); padding: .3rem .6rem;
}
.sg-status .sg-cursor{ display:inline-block; color: var(--brass-bright); animation: blink 1.1s step-end infinite; }
@media (max-width: 640px){ .sg-status{ display: none; } }

/* ---------------------------------------------------------------- */
/* Hero / field-note card                                            */
/* ---------------------------------------------------------------- */
.sg-hero{
  background: var(--bg-raised);
  border: 1px solid var(--line-strong);
  padding: 1.4rem 1.6rem;
  animation: fadeUp .5s var(--ease);
}
.sg-hero .sg-tag{ margin-bottom: .5rem; }
.sg-hero h3{ margin: 0 0 .35rem 0; font-family: 'Newsreader', serif; font-weight: 500; font-size: 1.15rem; }
.sg-hero p{ margin: 0; color: var(--ink-muted); font-size: .9rem; }

/* Chat bubbles */
[data-testid="stChatMessage"]{
  background: var(--bg-raised) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 2px !important;
  box-shadow: var(--shadow-1);
  animation: fadeUp .3s var(--ease);
}

/* Buttons — stamped brass label, not a glossy 3D pill */
.stButton > button, .stDownloadButton > button{
  background: var(--brass) !important;
  color: #17110a !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-weight: 500 !important;
  font-size: .8rem !important;
  letter-spacing: .04em !important;
  text-transform: uppercase !important;
  border: 1px solid var(--brass) !important;
  border-radius: 2px !important;
  box-shadow: none !important;
  transition: background .18s, transform .12s var(--ease) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  background: var(--brass-bright) !important;
  transform: translateY(-1px);
}
.stButton > button:active, .stDownloadButton > button:active{ transform: translateY(1px); }

section[data-testid="stSidebar"] .stButton > button{
  background: var(--bg-raised-2) !important; color: var(--ink) !important;
  border: 1px solid var(--line-strong) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover{ border-color: var(--brass) !important; }

[data-testid="stToggle"] label div[data-checked="true"]{ background: var(--brass) !important; }

[data-testid="stChatInput"]{
  border: 1px solid var(--line-strong) !important;
  border-radius: 2px !important;
  background: var(--bg-raised) !important;
}

[data-testid="stFileUploaderDropzone"]{
  background: var(--bg-raised) !important;
  border: 1px dashed var(--line-strong) !important;
  border-radius: 2px !important;
  transition: border-color .2s;
}
[data-testid="stFileUploaderDropzone"]:hover{ border-color: var(--brass) !important; }

/* ---------------------------------------------------------------- */
/* Footer — an engineering drawing title block                       */
/* ---------------------------------------------------------------- */
.sg-footer{ margin: 3rem -1rem -1rem -1rem; padding: 0 1.5rem 1.4rem 1.5rem; }
.sg-titleblock{
  max-width: 960px; margin: 0 auto;
  border: 1px solid var(--line-strong);
  background: var(--bg-raised);
}
.sg-tb-head{
  display: flex; align-items: center; gap: .6rem;
  padding: .7rem 1rem; border-bottom: 1px solid var(--line-strong);
}
.sg-tb-head .sg-brand-mark{ width: 22px; height: 22px; padding: 3px; animation: none; }
.sg-tb-head span{
  font-family: 'IBM Plex Mono', monospace; font-size: .7rem; letter-spacing: .1em;
  text-transform: uppercase; color: var(--ink-muted);
}
.sg-tb-grid{ display: grid; grid-template-columns: repeat(4, 1fr); }
@media (max-width: 700px){ .sg-tb-grid{ grid-template-columns: repeat(2, 1fr); } }
.sg-tb-cell{ padding: .9rem 1rem; border-right: 1px solid var(--line-strong); border-top: 1px solid var(--line-strong); }
.sg-tb-cell:nth-child(4n){ border-right: none; }
.sg-tb-label{
  font-family: 'IBM Plex Mono', monospace; font-size: .62rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--ink-faint); margin-bottom: .3rem; display: block;
}
.sg-tb-value{ font-size: .85rem; color: var(--ink); line-height: 1.5; }
.sg-tb-value a{ color: var(--brass-bright); text-decoration: none; border-bottom: 1px solid rgba(226,169,80,.35); }
.sg-tb-value a:hover{ border-color: var(--brass-bright); }
.sg-tb-bottom{
  padding: .55rem 1rem; border-top: 1px solid var(--line-strong);
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: .4rem;
  font-family: 'IBM Plex Mono', monospace; font-size: .65rem; color: var(--ink-faint);
}
"""


def inject_theme() -> None:
    """Injects fonts + global CSS. Call once, right after st.set_page_config()."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Sticky instrument-panel header with the drawn leaf mark and a terminal-style status tag."""
    st.markdown(
        f"""
        <div class="sg-header">
          <div class="sg-brand">
            <div class="sg-brand-mark">{LEAF_SVG}</div>
            <div>
              <div class="sg-word">Sage AI</div>
              <div class="sg-tag">Document &amp; Code Intelligence</div>
            </div>
          </div>
          <div class="sg-status">STATUS: ACTIVE<span class="sg-cursor">▌</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Field-note style welcome card, framed like a diagram callout."""
    st.markdown(
        """
        <div class="sg-hero sg-frame">
          <div class="sg-tag">Field Note — Getting Started</div>
          <h3>Ask a question, upload a document, or ask for some code.</h3>
          <p>Try: "Summarize this document" or "Write a function to check if a number is prime"</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Footer built as an engineering-drawing title block instead of a generic link list."""
    st.markdown(
        f"""
        <div class="sg-footer">
          <div class="sg-titleblock">
            <div class="sg-tb-head">
              <div class="sg-brand-mark">{LEAF_SVG}</div>
              <span>Sage AI — Title Block</span>
            </div>
            <div class="sg-tb-grid">
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Project</span>
                <div class="sg-tb-value">Sage AI — document &amp; code assistant</div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Modules</span>
                <div class="sg-tb-value">Chat · RAG · Code Exec</div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Stack</span>
                <div class="sg-tb-value">Groq · Streamlit · ChromaDB</div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Drawn By</span>
                <div class="sg-tb-value">{AUTHOR}</div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Rev</span>
                <div class="sg-tb-value">2026.1</div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Source</span>
                <div class="sg-tb-value"><a href="{GITHUB_URL}" target="_blank">GitHub ↗</a></div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">Live</span>
                <div class="sg-tb-value"><a href="{LIVE_URL}" target="_blank">Demo ↗</a></div>
              </div>
              <div class="sg-tb-cell">
                <span class="sg-tb-label">License</span>
                <div class="sg-tb-value">Personal project</div>
              </div>
            </div>
            <div class="sg-tb-bottom">
              <span>© 2026 SAGE AI</span>
              <span>SHEET 1 OF 1</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
