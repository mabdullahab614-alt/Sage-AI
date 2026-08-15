"""
Sage AI custom theme.

Design system:
- Colors chosen deliberately (not Streamlit defaults):
    Sage green   -> the literal plant color the brand is named after.
                    Psychologically: wisdom, calm, balance, growth.
    Warm charcoal -> depth and focus without the flat "pure black" look.
    Warm gold     -> confidence/warmth accent for primary actions.
    Warm ivory    -> softer than pure white, easier on the eyes for long chats.
- Type system: a characterful serif for the wordmark/headers (Fraunces),
  a warm humanist sans for body/chat text (Plus Jakarta Sans), and a
  proper coding monospace for code blocks (JetBrains Mono).
- One signature move: a small breathing leaf mark next to the wordmark,
  everything else stays disciplined (consistent spacing, restrained motion).
"""

PAGE_TITLE = "Sage AI — AI Document & Code Assistant"
PAGE_DESCRIPTION = (
    "Sage AI is a free AI assistant for chat, document Q&A (RAG over PDF, "
    "Word, Excel, and CSV files), and Python code generation with live "
    "execution — built by Abdullah Javed."
)
PAGE_ICON = "🌿"

FONT_IMPORTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""

CUSTOM_CSS = """
<style>
:root {
    --sage: #8FAE7C;
    --sage-deep: #5C7A4E;
    --sage-glow: rgba(143, 174, 124, 0.35);
    --gold: #D9A94E;
    --gold-deep: #B98A34;
    --bg-deep: #14181A;
    --bg-panel: #1B211C;
    --bg-panel-raised: #212820;
    --ink: #EDEAE0;
    --muted: #9CA394;
    --error: #E2725B;
    --border: rgba(143, 174, 124, 0.18);
    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'Plus Jakarta Sans', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', 'Courier New', monospace;
}

/* ---------- Base ---------- */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(143, 174, 124, 0.08), transparent),
        var(--bg-deep) !important;
    color: var(--ink) !important;
}

/* ---------- Custom scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
    background: var(--sage-deep);
    border-radius: 8px;
    border: 2px solid var(--bg-deep);
}
::-webkit-scrollbar-thumb:hover { background: var(--sage); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--ink); }

/* ---------- Wordmark / header ---------- */
.sage-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.25rem 0 0.5rem 0;
}
.sage-leaf-mark {
    font-size: 1.9rem;
    display: inline-block;
    animation: sage-breathe 3.6s ease-in-out infinite;
    filter: drop-shadow(0 0 6px var(--sage-glow));
}
@keyframes sage-breathe {
    0%, 100% { transform: scale(1); opacity: 0.92; }
    50%      { transform: scale(1.08); opacity: 1; }
}
.sage-wordmark {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 1.7rem;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0;
    line-height: 1;
}
.sage-tagline {
    font-family: var(--font-body);
    color: var(--muted);
    font-size: 0.92rem;
    margin-top: 0.15rem;
}
.sage-eyebrow {
    font-family: var(--font-body);
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sage);
    margin-bottom: 0.35rem;
}

/* ---------- Sidebar section cards ---------- */
.sage-card {
    background: var(--bg-panel-raised);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.9rem;
}

/* ---------- Buttons: hover lift, press, ripple, focus glow ---------- */
.stButton > button, [data-testid="stChatInput"] button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-deep)) !important;
    color: var(--bg-deep) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: var(--font-body) !important;
    letter-spacing: 0.01em;
    padding: 0.5rem 1.1rem !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(217, 169, 78, 0.35);
    filter: brightness(1.06);
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(0px) scale(0.98);
    box-shadow: 0 2px 6px rgba(217, 169, 78, 0.25);
}
.stButton > button:focus-visible {
    outline: 2px solid var(--sage) !important;
    outline-offset: 2px;
}

/* Secondary / utility buttons (clear conversation, clear docs) get a quieter treatment */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    color: var(--sage) !important;
    border-color: var(--sage) !important;
    background: rgba(143, 174, 124, 0.08) !important;
    box-shadow: 0 0 0 3px var(--sage-glow);
}

/* ---------- Chat messages: fade/slide in, distinct user vs assistant tone ---------- */
[data-testid="stChatMessage"] {
    animation: sage-msg-in 0.35s ease-out;
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    padding: 0.25rem 0.4rem !important;
    margin-bottom: 0.6rem !important;
}
@keyframes sage-msg-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, var(--gold), var(--gold-deep)) !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, var(--sage), var(--sage-deep)) !important;
}

/* ---------- Chat input: focus glow ---------- */
[data-testid="stChatInput"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: var(--bg-panel-raised) !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--sage) !important;
    box-shadow: 0 0 0 4px var(--sage-glow) !important;
}

/* ---------- Toggle switch ---------- */
[data-testid="stToggle"] label div[data-checked="true"] {
    background: var(--sage) !important;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] section {
    background: var(--bg-panel-raised) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease, background 0.2s ease;
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--sage) !important;
    background: rgba(143, 174, 124, 0.06) !important;
}

/* ---------- Code blocks ---------- */
code, pre, .stCodeBlock, [data-testid="stCodeBlock"] {
    font-family: var(--font-mono) !important;
}
[data-testid="stCodeBlock"] {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ---------- Alerts (success/error/warning) recolored to fit palette ---------- */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ---------- Divider ---------- */
hr { border-color: var(--border) !important; }

/* ---------- Footer signature ---------- */
.sage-footer {
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    font-family: var(--font-body);
}
.sage-footer a {
    color: var(--sage);
    text-decoration: none;
    font-weight: 600;
}
.sage-footer a:hover { text-decoration: underline; }

/* ---------- Respect reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
    .sage-leaf-mark, [data-testid="stChatMessage"] {
        animation: none !important;
    }
}
</style>
"""

# Best-effort SEO/meta tags. Streamlit is a client-rendered app, so this
# will not produce full server-side-rendered SEO the way a static site
# would, but it does set the browser tab title, favicon, and description
# meta tag used by link previews / some crawlers.
SEO_INJECTION = f"""
<script>
    try {{
        const doc = window.parent.document;
        doc.title = "{PAGE_TITLE}";

        function setMeta(name, content, isProperty) {{
            const attr = isProperty ? "property" : "name";
            let tag = doc.querySelector(`meta[${{attr}}="${{name}}"]`);
            if (!tag) {{
                tag = doc.createElement("meta");
                tag.setAttribute(attr, name);
                doc.head.appendChild(tag);
            }}
            tag.setAttribute("content", content);
        }}

        setMeta("description", "{PAGE_DESCRIPTION}", false);
        setMeta("og:title", "{PAGE_TITLE}", true);
        setMeta("og:description", "{PAGE_DESCRIPTION}", true);
        setMeta("og:type", "website", true);
        setMeta("twitter:card", "summary", true);
        setMeta("twitter:title", "{PAGE_TITLE}", true);
        setMeta("twitter:description", "{PAGE_DESCRIPTION}", true);
    }} catch (e) {{
        // Cross-origin/frame restrictions can block this in some embeds;
        // fail silently since it's a progressive enhancement, not required.
    }}
</script>
"""


def inject_theme(st_module):
    """Call once near the top of app.py to apply fonts, CSS, and SEO tags."""
    st_module.markdown(FONT_IMPORTS, unsafe_allow_html=True)
    st_module.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st_module.components.v1.html(SEO_INJECTION, height=0, width=0)


def render_header(st_module):
    """Signature wordmark + tagline, used both in sidebar and main area."""
    st_module.markdown(
        """
        <div class="sage-header">
            <span class="sage-leaf-mark">🌿</span>
            <div>
                <p class="sage-wordmark">Sage AI</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer(st_module):
    st_module.markdown(
        """
        <div class="sage-footer">
            Built by <a href="https://github.com/mabdullahab614-alt" target="_blank">Abdullah Javed</a>
            &nbsp;·&nbsp; Powered by Groq (Llama 3.3) &nbsp;·&nbsp;
            <a href="https://github.com/mabdullahab614-alt/Sage-AI" target="_blank">View source</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
