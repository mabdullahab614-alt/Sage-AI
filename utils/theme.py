"""
Sage AI — visual theme.

Design language: "reading room, not a dashboard." A calm, solid forest-charcoal
surface with a single warm gold accent (the pen/ink of an old field journal),
a breathing leaf mark as the signature motif, and restrained 3D depth on
interactive elements rather than blanket glassmorphism. The header is the one
place that gets a real glass treatment (frosted, sticky, floating above the
scroll) — everything else uses solid, opaque surfaces so text stays crisp.

Usage (top of app.py, right after st.set_page_config):

    from utils.theme import inject_theme, render_header, render_footer

    inject_theme()
    render_header()
    ... existing app body ...
    render_footer()
"""

import streamlit as st

GITHUB_URL = "https://github.com/mabdullahab614-alt/Sage-AI"
LIVE_URL = "https://sage-ai-q9bvrp6nmajtrxp9rp9zna.streamlit.app"
AUTHOR = "Abdullah Javed"

_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root{
  --bg:            #0e1512;
  --bg-raised:     #161f1a;
  --bg-raised-2:   #1d2921;
  --sage:          #4f7a5c;
  --sage-light:    #8db097;
  --gold:          #cf9f3f;
  --gold-bright:   #e7bf68;
  --ink:           #f1ede2;
  --ink-muted:     #9fab9f;
  --ink-faint:     #6d786e;
  --border:        rgba(207,159,63,0.16);
  --border-soft:   rgba(241,237,226,0.08);
  --shadow-1:      0 1px 2px rgba(0,0,0,.35);
  --shadow-2:      0 8px 24px rgba(0,0,0,.38);
  --shadow-3:      0 18px 40px rgba(0,0,0,.45);
  --ease:          cubic-bezier(.22,.9,.32,1.15);
}

@media (prefers-reduced-motion: reduce){
  *{ animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }
}

html, body, [class*="css"]{
  font-family: 'Inter', -apple-system, sans-serif;
}

.stApp{
  background:
    radial-gradient(1200px 600px at 15% -10%, rgba(79,122,92,.16), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, rgba(207,159,63,.08), transparent 55%),
    var(--bg);
  color: var(--ink);
}

section[data-testid="stSidebar"]{
  background: var(--bg-raised);
  border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] *{ color: var(--ink); }

.block-container{ padding-top: 1rem; max-width: 980px; }

/* Scrollbar */
::-webkit-scrollbar{ width: 10px; height: 10px; }
::-webkit-scrollbar-track{ background: var(--bg); }
::-webkit-scrollbar-thumb{ background: var(--bg-raised-2); border-radius: 8px; border: 2px solid var(--bg); }
::-webkit-scrollbar-thumb:hover{ background: var(--sage); }

:focus-visible{ outline: 2px solid var(--gold-bright); outline-offset: 2px; border-radius: 4px; }

/* ---------------------------------------------------------------- */
/* Motion                                                            */
/* ---------------------------------------------------------------- */
@keyframes breathe{
  0%,100%{ transform: scale(1) rotate(-2deg); filter: drop-shadow(0 0 0 rgba(207,159,63,0)); }
  50%{ transform: scale(1.07) rotate(1deg); filter: drop-shadow(0 0 10px rgba(207,159,63,.45)); }
}
@keyframes fadeUp{
  from{ opacity: 0; transform: translateY(10px); }
  to{ opacity: 1; transform: translateY(0); }
}
@keyframes floatIn{
  from{ opacity: 0; transform: translateY(-6px); }
  to{ opacity: 1; transform: translateY(0); }
}
@keyframes pulseDot{
  0%{ box-shadow: 0 0 0 0 rgba(143,196,146,.55); }
  70%{ box-shadow: 0 0 0 7px rgba(143,196,146,0); }
  100%{ box-shadow: 0 0 0 0 rgba(143,196,146,0); }
}
@keyframes shimmer{
  0%{ background-position: -200% 0; }
  100%{ background-position: 200% 0; }
}

/* ---------------------------------------------------------------- */
/* Header — the one glass surface                                    */
/* ---------------------------------------------------------------- */
.sg-header{
  position: sticky;
  top: 0;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin: -1rem -1rem 1.5rem -1rem;
  padding: .85rem 1.5rem;
  background: rgba(20,28,23,.62);
  backdrop-filter: blur(14px) saturate(140%);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-2);
  animation: floatIn .5s var(--ease);
}
.sg-brand{ display: flex; align-items: center; gap: .7rem; }
.sg-mark{
  font-size: 1.6rem;
  line-height: 1;
  display: inline-block;
  animation: breathe 4.5s ease-in-out infinite;
  filter: drop-shadow(0 2px 3px rgba(0,0,0,.4));
}
.sg-word{
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: 1.35rem;
  letter-spacing: .01em;
  color: var(--ink);
  background: linear-gradient(90deg, var(--ink) 40%, var(--gold-bright) 48%, var(--ink) 56%);
  background-size: 250% 100%;
  -webkit-background-clip: text;
  background-clip: text;
}
.sg-brand:hover .sg-word{ animation: shimmer 2.2s linear infinite; }
.sg-tag{
  font-family: 'JetBrains Mono', monospace;
  font-size: .68rem;
  color: var(--ink-faint);
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-top: 2px;
}
.sg-pills{ display: flex; align-items: center; gap: .5rem; }
.sg-pill{
  font-family: 'JetBrains Mono', monospace;
  font-size: .68rem;
  letter-spacing: .04em;
  color: var(--ink-muted);
  background: rgba(255,255,255,.03);
  border: 1px solid var(--border-soft);
  padding: .3rem .65rem;
  border-radius: 999px;
  transition: transform .2s var(--ease), border-color .2s, color .2s;
}
.sg-pill:hover{ transform: translateY(-2px); border-color: var(--gold); color: var(--gold-bright); }
.sg-status{
  display: flex; align-items: center; gap: .4rem;
  font-family: 'JetBrains Mono', monospace; font-size: .68rem; color: var(--sage-light);
}
.sg-dot{ width: 7px; height: 7px; border-radius: 50%; background: #8fc492; animation: pulseDot 2.2s infinite; }

@media (max-width: 640px){
  .sg-pills{ display: none; }
}

/* ---------------------------------------------------------------- */
/* Cards / surfaces                                                  */
/* ---------------------------------------------------------------- */
.sg-hero{
  background: linear-gradient(165deg, var(--bg-raised) 0%, var(--bg-raised-2) 100%);
  border: 1px solid var(--border-soft);
  border-left: 3px solid var(--sage);
  border-radius: 14px;
  padding: 1.4rem 1.6rem;
  box-shadow: var(--shadow-2);
  animation: fadeUp .5s var(--ease);
  transition: transform .35s var(--ease), box-shadow .35s var(--ease);
}
.sg-hero:hover{ transform: translateY(-3px) perspective(600px) rotateX(1deg); box-shadow: var(--shadow-3); }
.sg-hero h3{ margin: 0 0 .3rem 0; font-family: 'Fraunces', serif; font-weight: 600; }
.sg-hero p{ margin: 0; color: var(--ink-muted); font-size: .92rem; }

/* Chat bubbles */
[data-testid="stChatMessage"]{
  background: var(--bg-raised) !important;
  border: 1px solid var(--border-soft);
  border-radius: 12px;
  box-shadow: var(--shadow-1);
  animation: fadeUp .35s var(--ease);
  transition: box-shadow .25s var(--ease), transform .25s var(--ease);
}
[data-testid="stChatMessage"]:hover{ box-shadow: var(--shadow-2); transform: translateY(-1px); }

/* Buttons — solid, with a physical 3D press */
.stButton > button, .stDownloadButton > button{
  background: linear-gradient(180deg, var(--gold-bright), var(--gold)) !important;
  color: #1c1206 !important;
  font-weight: 600 !important;
  border: none !important;
  border-radius: 10px !important;
  box-shadow: 0 3px 0 #8a6a25, var(--shadow-1) !important;
  transition: transform .12s var(--ease), box-shadow .12s var(--ease) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  transform: translateY(-2px);
  box-shadow: 0 5px 0 #8a6a25, var(--shadow-2) !important;
}
.stButton > button:active, .stDownloadButton > button:active{
  transform: translateY(2px);
  box-shadow: 0 1px 0 #8a6a25 !important;
}

/* Secondary / sidebar buttons keep it quiet */
section[data-testid="stSidebar"] .stButton > button{
  background: var(--bg-raised-2) !important;
  color: var(--ink) !important;
  box-shadow: var(--shadow-1) !important;
  border: 1px solid var(--border-soft) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover{
  border-color: var(--gold) !important;
  box-shadow: var(--shadow-2) !important;
}

/* Toggle accent */
[data-testid="stToggle"] label div[data-checked="true"]{ background: var(--sage) !important; }

/* Chat input */
[data-testid="stChatInput"]{
  border: 1px solid var(--border-soft) !important;
  border-radius: 12px !important;
  background: var(--bg-raised) !important;
  box-shadow: var(--shadow-2) !important;
}

/* File uploader card */
[data-testid="stFileUploaderDropzone"]{
  background: var(--bg-raised) !important;
  border: 1px dashed var(--border) !important;
  border-radius: 12px !important;
  transition: border-color .2s, transform .2s var(--ease);
}
[data-testid="stFileUploaderDropzone"]:hover{ border-color: var(--gold-bright) !important; transform: translateY(-2px); }

/* ---------------------------------------------------------------- */
/* Footer — solid, structured, multi-column                          */
/* ---------------------------------------------------------------- */
.sg-footer{
  margin: 3rem -1rem -1rem -1rem;
  padding: 2.2rem 1.6rem 1.4rem 1.6rem;
  background: var(--bg-raised);
  border-top: 1px solid transparent;
  border-image: linear-gradient(90deg, transparent, var(--gold), transparent) 1;
  box-shadow: 0 -10px 30px rgba(0,0,0,.25);
}
.sg-footer-grid{
  display: grid;
  grid-template-columns: 1.3fr 1fr 1fr;
  gap: 2rem;
  max-width: 980px;
  margin: 0 auto;
}
@media (max-width: 700px){ .sg-footer-grid{ grid-template-columns: 1fr; } }

.sg-footer h4{
  font-family: 'Fraunces', serif;
  font-size: .95rem;
  color: var(--ink);
  margin: 0 0 .6rem 0;
}
.sg-footer p, .sg-footer li{
  color: var(--ink-muted);
  font-size: .85rem;
  line-height: 1.6;
}
.sg-footer ul{ list-style: none; padding: 0; margin: 0; }
.sg-footer li{ display: flex; align-items: center; gap: .45rem; margin-bottom: .35rem; }
.sg-footer li::before{ content: "◆"; color: var(--sage-light); font-size: .5rem; }

.sg-footer-links a{
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  color: var(--ink);
  text-decoration: none;
  font-size: .85rem;
  padding: .4rem .7rem;
  margin: 0 .3rem .4rem 0;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  background: var(--bg-raised-2);
  transition: transform .2s var(--ease), border-color .2s, box-shadow .2s var(--ease);
}
.sg-footer-links a:hover{
  transform: translateY(-2px);
  border-color: var(--gold);
  box-shadow: var(--shadow-2);
  color: var(--gold-bright);
}

.sg-footer-bottom{
  max-width: 980px;
  margin: 1.6rem auto 0 auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border-soft);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: .5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .72rem;
  color: var(--ink-faint);
}
.sg-footer-bottom .sg-mark{ font-size: 1rem; margin-right: .3rem; animation-duration: 6s; }
</style>
"""


def inject_theme() -> None:
    """Injects fonts + global CSS. Call once, right after st.set_page_config()."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Sticky, frosted-glass header with the breathing leaf mark and feature pills."""
    st.markdown(
        """
        <div class="sg-header">
          <div class="sg-brand">
            <span class="sg-mark">🌿</span>
            <div>
              <div class="sg-word">Sage AI</div>
              <div class="sg-tag">document &amp; code intelligence</div>
            </div>
          </div>
          <div class="sg-pills">
            <span class="sg-pill">Chat</span>
            <span class="sg-pill">Documents · RAG</span>
            <span class="sg-pill">Code Exec</span>
          </div>
          <div class="sg-status"><span class="sg-dot"></span>Online</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Solid, structured multi-column footer."""
    st.markdown(
        f"""
        <div class="sg-footer">
          <div class="sg-footer-grid">
            <div>
              <h4>🌿 Sage AI</h4>
              <p>A single-page assistant for grounded conversation, document
              understanding, and Python you can actually run — built to stay
              out of your way and get the answer right.</p>
            </div>
            <div>
              <h4>Capabilities</h4>
              <ul>
                <li>General chat with memory</li>
                <li>RAG over PDF · Word · Excel · CSV</li>
                <li>Python generation &amp; sandboxed execution</li>
              </ul>
            </div>
            <div>
              <h4>Connect</h4>
              <div class="sg-footer-links">
                <a href="{GITHUB_URL}" target="_blank">↗ Source on GitHub</a>
                <a href="{LIVE_URL}" target="_blank">↗ Live demo</a>
              </div>
            </div>
          </div>
          <div class="sg-footer-bottom">
            <span><span class="sg-mark">🌿</span>© 2026 Sage AI — built by {AUTHOR}</span>
            <span>Powered by Groq · Streamlit · ChromaDB</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
