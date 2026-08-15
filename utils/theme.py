"""
Sage AI — visual theme.

Design language: "a naturalist's field notebook, drafted like a blueprint" —
now in a light parchment palette instead of dark. Solid, opaque fills
throughout (no glass/blur, no gradients) in cream, deep sage green, and
walnut brown. A drawn line-art leaf diagram stands in for the brand mark.
Cards are framed like technical-drawing callouts with corner registration
marks. The footer is an engineering title block.

The header is a normal (non-sticky) block with generous height and a solid
background — earlier versions used `position: sticky` plus a negative
edge-bleed margin, which on Streamlit Cloud fought with the platform's own
fixed toolbar and made the header disappear. This version just sits in
normal document flow, tall and unmissable.

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
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root{
  --bg:            #f7f1e3;
  --bg-raised:     #fffcf5;
  --bg-raised-2:   #efe4cb;
  --green:         #3c5a37;
  --green-dark:    #2a4126;
  --brown:         #7a5230;
  --brown-dark:    #593a20;
  --ink:           #2a2015;
  --ink-muted:     #6c6252;
  --ink-faint:     #978c78;
  --line:          rgba(42,32,21,0.14);
  --line-strong:   rgba(42,32,21,0.28);
  --shadow-1:      0 1px 3px rgba(42,32,21,.10);
  --shadow-2:      0 8px 22px rgba(42,32,21,.14);
  --ease:          cubic-bezier(.2,.75,.3,1);

  /* dark surface, used only for header / footer / buttons — the
     deliberate "mix" against the light parchment body */
  --dark:          #23301f;
  --dark-2:        #2f3f27;
  --dark-line:     rgba(247,241,227,0.14);
  --cream:         #f4ecd8;
  --gold:          #d3a34f;
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
  background: var(--bg-raised-2);
  border-right: 1px solid var(--line-strong);
}
section[data-testid="stSidebar"] *{ color: var(--ink); }
section[data-testid="stSidebar"] h1{ color: var(--green-dark); }

.block-container{ padding-top: 1.5rem; padding-bottom: 6rem; max-width: 960px; }

/* Streamlit's fixed bottom bar that holds the chat input — retheme it so it
   doesn't sit there as an unstyled black strip, and stop it covering the
   last rows of page content (like the footer title block) as you scroll. */
div[data-testid="stBottom"], .stChatFloatingInputContainer{
  background: var(--bg) !important;
  border-top: 1px solid var(--line-strong) !important;
}
div[data-testid="stBottom"] > div{ background: var(--bg) !important; }

::-webkit-scrollbar{ width: 9px; height: 9px; }
::-webkit-scrollbar-track{ background: var(--bg); }
::-webkit-scrollbar-thumb{ background: var(--bg-raised-2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover{ background: var(--brown); }
:focus-visible{ outline: 1.5px solid var(--brown); outline-offset: 2px; }

.sg-leaf-svg{ width: 100%; height: 100%; color: var(--green-dark); display: block; }

@keyframes fadeUp{ from{ opacity:0; transform: translateY(8px);} to{ opacity:1; transform: translateY(0);} }
@keyframes blink{ 0%,49%{ opacity:1;} 50%,100%{ opacity:0;} }
@keyframes sway{ 0%,100%{ transform: rotate(-3deg);} 50%{ transform: rotate(3deg);} }

/* ---------------------------------------------------------------- */
/* Corner-bracket frame — shared "technical drawing" motif           */
/* ---------------------------------------------------------------- */
.sg-frame{ position: relative; }
.sg-frame::before, .sg-frame::after{
  content: ""; position: absolute; width: 12px; height: 12px;
  border: 1.5px solid var(--brown); opacity: .85; transition: width .25s var(--ease), height .25s var(--ease);
}
.sg-frame::before{ top: -1px; left: -1px; border-right: none; border-bottom: none; }
.sg-frame::after{ bottom: -1px; right: -1px; border-left: none; border-top: none; }
.sg-frame:hover::before, .sg-frame:hover::after{ width: 18px; height: 18px; }

/* ---------------------------------------------------------------- */
/* Header — tall, solid, sits in normal flow (no sticky/edge-bleed)  */
/* ---------------------------------------------------------------- */
.sg-header{
  display: flex; align-items: center; justify-content: space-between; gap: 1.2rem;
  width: 100%;
  margin: 0 0 1.8rem 0;
  padding: 1.5rem 2rem;
  background: var(--dark);
  border: 1px solid var(--dark-line);
  border-left: 5px solid var(--gold);
  border-radius: 4px;
  box-shadow: var(--shadow-2);
  animation: fadeUp .4s var(--ease);
  box-sizing: border-box;
}
.sg-brand{ display: flex; align-items: center; gap: 1rem; }
.sg-header .sg-brand-mark{
  width: 52px; height: 52px; padding: 9px;
  background: var(--dark-2);
  border: 1px solid var(--dark-line); border-radius: 6px;
  animation: sway 6s ease-in-out infinite; transform-origin: 50% 90%;
  flex-shrink: 0;
}
.sg-header .sg-leaf-svg{ color: var(--gold); }
.sg-header .sg-word{
  font-family: 'Newsreader', serif; font-weight: 700; font-size: 2.1rem;
  letter-spacing: .01em; color: var(--cream); line-height: 1.05;
}
.sg-header .sg-tag{
  font-family: 'IBM Plex Mono', monospace; font-size: .72rem; color: var(--gold);
  letter-spacing: .09em; text-transform: uppercase; margin-top: 4px;
}
.sg-status{
  font-family: 'IBM Plex Mono', monospace; font-size: .74rem; letter-spacing: .04em;
  color: var(--cream); border: 1px solid var(--dark-line);
  background: var(--dark-2);
  padding: .5rem .85rem; border-radius: 3px; white-space: nowrap;
}
.sg-status .sg-cursor{ display:inline-block; color: var(--gold); animation: blink 1.1s step-end infinite; }
@media (max-width: 680px){
  .sg-header{ flex-direction: column; align-items: flex-start; gap: .8rem; }
  .sg-status{ align-self: flex-start; }
}

/* ---------------------------------------------------------------- */
/* Hero / field-note card                                            */
/* ---------------------------------------------------------------- */
.sg-hero{
  background: var(--bg-raised);
  border: 1px solid var(--line-strong);
  padding: 1.4rem 1.6rem;
  border-radius: 4px;
  box-shadow: var(--shadow-1);
  animation: fadeUp .5s var(--ease);
}
.sg-hero .sg-tag{ margin-bottom: .5rem; color: var(--green-dark); }
.sg-hero h3{ margin: 0 0 .35rem 0; font-family: 'Newsreader', serif; font-weight: 500; font-size: 1.2rem; color: var(--ink); }
.sg-hero p{ margin: 0; color: var(--ink-muted); font-size: .9rem; }

/* Chat bubbles */
[data-testid="stChatMessage"]{
  background: var(--bg-raised) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 4px !important;
  box-shadow: var(--shadow-1);
  animation: fadeUp .3s var(--ease);
}
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li{ color: var(--ink) !important; }

/* Buttons — solid dark fill, small radius, mono label */
.stButton > button, .stDownloadButton > button{
  background: var(--dark) !important;
  color: var(--cream) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-weight: 600 !important;
  font-size: .8rem !important;
  letter-spacing: .04em !important;
  text-transform: uppercase !important;
  border: 1px solid var(--dark) !important;
  border-radius: 3px !important;
  box-shadow: none !important;
  transition: background .18s, transform .12s var(--ease) !important;
}
.stButton > button *, .stDownloadButton > button *{ color: var(--cream) !important; }
.stButton > button:hover, .stDownloadButton > button:hover{
  background: var(--dark-2) !important;
  color: var(--gold) !important;
  border-color: var(--gold) !important;
  transform: translateY(-1px);
}
.stButton > button:hover *, .stDownloadButton > button:hover *{ color: var(--gold) !important; }
.stButton > button:active, .stDownloadButton > button:active{ transform: translateY(1px); }

section[data-testid="stSidebar"] .stButton > button{
  background: var(--dark) !important; color: var(--cream) !important;
  border: 1px solid var(--dark) !important;
}
section[data-testid="stSidebar"] .stButton > button *{ color: var(--cream) !important; }
section[data-testid="stSidebar"] .stButton > button:hover{ background: var(--dark-2) !important; color: var(--gold) !important; border-color: var(--gold) !important; }
section[data-testid="stSidebar"] .stButton > button:hover *{ color: var(--gold) !important; }

[data-testid="stToggle"] label div[data-checked="true"]{ background: var(--green) !important; }

[data-testid="stChatInput"]{
  border: 1px solid var(--line-strong) !important;
  border-radius: 4px !important;
  background: var(--bg-raised) !important;
}
[data-testid="stChatInput"] textarea{ color: var(--ink) !important; }

[data-testid="stFileUploaderDropzone"]{
  background: var(--bg-raised) !important;
  border: 1px dashed var(--line-strong) !important;
  border-radius: 4px !important;
  transition: border-color .2s;
}
[data-testid="stFileUploaderDropzone"]:hover{ border-color: var(--brown) !important; }

/* ---------------------------------------------------------------- */
/* Footer — engineering drawing title block                          */
/* ---------------------------------------------------------------- */
.sg-footer{ margin: 3rem 0 0 0; }
.sg-titleblock{
  border: 1px solid var(--dark-line);
  background: var(--dark);
  border-radius: 4px;
  box-shadow: var(--shadow-2);
}
.sg-tb-head{
  display: flex; align-items: center; gap: .6rem;
  padding: .8rem 1.1rem; border-bottom: 1px solid var(--dark-line);
  background: var(--dark-2);
  border-radius: 4px 4px 0 0;
}
.sg-tb-head .sg-brand-mark{ width: 24px; height: 24px; padding: 3px; animation: none; background: transparent; border: none; }
.sg-tb-head .sg-leaf-svg{ color: var(--gold); }
.sg-tb-head span{
  font-family: 'IBM Plex Mono', monospace; font-size: .72rem; letter-spacing: .1em;
  text-transform: uppercase; color: var(--gold);
}
.sg-tb-grid{ display: grid; grid-template-columns: repeat(4, 1fr); }
@media (max-width: 700px){ .sg-tb-grid{ grid-template-columns: repeat(2, 1fr); } }
.sg-tb-cell{ padding: .9rem 1.1rem; border-right: 1px solid var(--dark-line); border-top: 1px solid var(--dark-line); }
.sg-tb-cell:nth-child(4n){ border-right: none; }
.sg-tb-label{
  font-family: 'IBM Plex Mono', monospace; font-size: .64rem; letter-spacing: .08em;
  text-transform: uppercase; color: rgba(244,236,216,.55); margin-bottom: .3rem; display: block;
}
.sg-tb-value{ font-size: .87rem; color: var(--cream); line-height: 1.5; }
.sg-tb-value a{ color: var(--gold); text-decoration: none; border-bottom: 1px solid var(--gold); font-weight: 500; }
.sg-tb-value a:hover{ color: var(--cream); border-color: var(--cream); }
.sg-tb-bottom{
  padding: .6rem 1.1rem; border-top: 1px solid var(--dark-line);
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: .4rem;
  font-family: 'IBM Plex Mono', monospace; font-size: .66rem; color: rgba(244,236,216,.55);
}
"""


def inject_theme() -> None:
    """Injects fonts + global CSS. Call once, right after st.set_page_config()."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Tall, solid header sitting in normal document flow — no sticky, no clipping."""
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
