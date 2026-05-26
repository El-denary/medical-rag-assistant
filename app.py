import streamlit as st
from state import State
from workflow import Workflow
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from db import init_db, create_session, save_message, load_messages, get_all_sessions

load_dotenv()

st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
            
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

:root {
    --bg:       #f4f9f6;
    --surface:  #ffffff;
    --border:   #c8e6d4;
    --green:    #27a35a;
    --green-l:  #eaf6f0;
    --green-d:  #1c7a42;
    --text:     #1a2e22;
    --muted:    #7a9a84;
    --user-bg:  #27a35a;
    --bot-bg:   #f0faf4;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ── fix black bar at bottom ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: var(--bg) !important;
    border-top: 1px solid var(--border) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container {
    max-width: 720px !important;
    padding: 0 1.5rem 2rem !important;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; 
            font-size: 13px !important;}

/* ── header ── */
.header {
    text-align: center;
    padding: 2.2rem 0 1.2rem;
}
.logo {
    font-size: 2.4rem;
    display: block;
    margin-bottom: 0.5rem;
    animation: popIn 0.4s ease;
}
@keyframes popIn {
    from { transform: scale(0.6); opacity: 0; }
    to   { transform: scale(1);   opacity: 1; }
}
.title {
    font-size: 1.9rem;
    font-weight: 600;
    color: var(--text);
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid var(--green);
    width: 0;
    animation: typing 2s steps(17, end) forwards,
               blink 0.75s step-end 4;
}
@keyframes typing {
    from { width: 0 }
    to   { width: 17ch }
}
@keyframes blink {
    0%, 100% { border-color: var(--green); }
    50%       { border-color: transparent; }
}
.subtitle {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.4rem;
    font-weight: 300;
}

hr.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0;
}

/* ── chat card ── */
.chat-card {
    background: var(--surface);
    border-radius: 16px;
    padding: 1.4rem;
    border: 1px solid var(--border);
    min-height: 240px;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 16px rgba(39,163,90,0.07);
}

/* ── messages ── */
.msg-row {
    display: flex;
    gap: 8px;
    margin-bottom: 0.9rem;
    align-items: flex-end;
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.avatar.user { background: var(--green); }
.avatar.bot  { background: var(--green-l); border: 1px solid var(--border); }

.bubble {
    max-width: 72%;
    padding: 11px 15px;
    font-size: 0.875rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble.user {
    background: var(--user-bg);
    color: #ffffff;
    border-radius: 16px 16px 4px 16px;
    box-shadow: 0 2px 8px rgba(39,163,90,0.2);
}
.bubble.bot {
    background: var(--bot-bg);
    color: var(--text);
    border-radius: 16px 16px 16px 4px;
    border: 1px solid var(--border);
}

/* ── empty state ── */
.empty {
    text-align: center;
    padding: 2.5rem 0;
    color: var(--muted);
    font-size: 0.82rem;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.hint-chip {
    display: inline-block;
    background: var(--green-l);
    color: var(--green-d);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4px 13px;
    margin: 3px;
    font-size: 0.72rem;
    font-weight: 500;
}

/* ── input ── */
[data-testid="stChatInput"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    background: var(--surface) !important;
    box-shadow: 0 2px 10px rgba(39,163,90,0.08) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px var(--green-l) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-size: 0.88rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
[data-testid="stChatInputSubmitButton"] svg { fill: var(--green) !important; }

/* ── buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    border-radius: 8px !important;
    padding: 0.35rem 1rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    text-align: left !important;
}
.stButton > button:hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
    background: var(--green-l) !important;
}

.stSpinner > div { border-top-color: var(--green) !important; }
</style>
""", unsafe_allow_html=True)

# ── init ──────────────────────────────────────────────────────
init_db()

if "session_id"  not in st.session_state: st.session_state.session_id  = create_session()
if "messages"    not in st.session_state: st.session_state.messages    = []
if "lc_messages" not in st.session_state: st.session_state.lc_messages = []
if "workflow"    not in st.session_state: st.session_state.workflow    = Workflow()

# ── sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🩺 Conversations")

    if st.button("＋  New Chat"):
        st.session_state.session_id  = create_session()
        st.session_state.messages    = []
        st.session_state.lc_messages = []
        st.rerun()

    st.markdown("<hr style='border-color:#c8e6d4;margin:0.8rem 0'>", unsafe_allow_html=True)

    sessions = get_all_sessions()
    if not sessions:
        st.markdown("<div style='font-size:0.75rem;color:#7a9a84;text-align:center;padding:1rem 0'>No past conversations yet.</div>", unsafe_allow_html=True)
    else:
        for s in sessions:
            label = s["first_message"][:30] + "..." if len(s["first_message"]) > 30 else s["first_message"]
            is_active = s["session_id"] == st.session_state.session_id
            icon = "🩺 " if is_active else " "
            if st.button(f"{icon}{label}", key=s["session_id"]):
                st.session_state.session_id  = s["session_id"]
                st.session_state.messages    = load_messages(s["session_id"])
                st.session_state.lc_messages = []
                st.rerun()

# ── header ────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <span class="logo">🩺</span>
    <div class="title">Medical Assistant</div>
    <div class="subtitle">Ask anything about diabetes</div>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── chat card ─────────────────────────────────────────────────
chat_html = '<div class="chat-card">'

if not st.session_state.messages:
    chat_html += """
    <div class="empty">
        <div class="empty-icon">💬</div>
        <div>Ask a question to get started</div>
        <div style="margin-top:0.9rem">
            <span class="hint-chip">What is diabetes?</span>
            <span class="hint-chip">Types of diabetes</span>
            <span class="hint-chip">Diabetes symptoms</span>
        </div>
    </div>"""
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="msg-row user">
                <div class="avatar user">👤</div>
                <div class="bubble user">{msg["content"]}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-row bot">
                <div class="avatar bot">🩺</div>
                <div class="bubble bot">{msg["content"]}</div>
            </div>"""

chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ── clear button ──────────────────────────────────────────────
if st.session_state.messages:
    col1, col2, col3 = st.columns([4, 2, 4])
    with col2:
        if st.button("🗑️  Clear"):
            st.session_state.messages    = []
            st.session_state.lc_messages = []
            st.session_state.session_id  = create_session()
            st.rerun()

# ── input ─────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about diabetes…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.session_id, "user", prompt)

    with st.spinner("Thinking…"):
        initial_state = State({
            "query":           prompt,
            "messages":        st.session_state.lc_messages[-4:],
            "content":         None,
            "response":        None,
            "rewritten_query": None,
        })
        result = st.session_state.workflow.run(initial_state)

    answer = result.get("response") or "Sorry, I could not find an answer."

    st.session_state.lc_messages.append(HumanMessage(content=prompt))
    st.session_state.lc_messages.append(AIMessage(content=answer))
    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_message(st.session_state.session_id, "assistant", answer)
    st.rerun()