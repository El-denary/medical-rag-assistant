<div align="center">

# 🩺 Medical RAG Assistant

**A conversational AI chatbot that answers medical questions using your own documents.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-MultiAgent-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-E85D4A?style=flat)](https://trychroma.com)
[![SQLite](https://img.shields.io/badge/SQLite-History-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)

*Stop searching. Just ask.*

</div>

---

## What Is This?

Medical RAG Assistant is a conversational AI system that lets you ask natural language questions about a medical PDF document and get accurate, grounded answers in seconds. Instead of reading through pages of documentation, you type your question and the system finds the right information and generates a clean response.

The system is built around a **3-agent pipeline** powered by LangGraph. Each query goes through query rewriting, vector retrieval, and response generation — automatically. Conversation history is saved to a local **SQLite database** so your chats persist across sessions.

---

## How It Works

```
User Question → Rewrite Agent → Retriever Agent → Response Agent → Answer
```

1. **Rewrite Agent** — rewrites the user's question to be more specific and retrieval-friendly
2. **Retriever Agent** — searches ChromaDB for the most relevant document chunks
3. **Response Agent** — reads the retrieved chunks and generates a concise, accurate answer

---

## Features

### 🤖 Multi-Agent Pipeline
- **LangGraph workflow** — 3 specialized agents connected in a stateful graph
- **Query rewriting** — improves retrieval accuracy by reformulating vague questions before searching
- **Stateful context** — last 4 messages of conversation history passed to each agent for multi-turn awareness

### 🔍 Retrieval Pipeline
- **ChromaDB vector store** — document chunks stored as dense vectors for semantic search
- **HuggingFace embeddings** — `all-MiniLM-L6-v2` model converts text to vectors locally, no API cost
- **Clean ingestion** — metadata stripped before storage, only `page_content` stored to minimize token usage
- **Configurable top-k** — retrieves top 3 chunks per query for focused, concise answers

### 💾 Persistent Conversation History
- **SQLite database** — every message saved automatically to `chat_history.db`
- **Session management** — each conversation gets a unique UUID, stored and retrievable
- **Full history UI** — sidebar shows all past conversations, click any to reload it
- **New chat anytime** — start a fresh conversation without losing previous ones

### 🎨 Clean Streamlit UI
- **Light green theme** — soft off-white background with green accents
- **Typewriter title animation** — title types itself out on load
- **Chat bubbles** — user messages in green, assistant replies in light green
- **Hint chips** — suggested questions shown on the empty state screen
- **Sidebar navigation** — all past conversations listed with active session highlighted

---

## System Architecture

```
┌─────────────────────────────────────────────────┐
│                  User (Browser)                 │
└──────────────────────┬──────────────────────────┘
                       │
              ┌────────▼────────┐
              │   Streamlit UI  │
              │  app.py         │
              │  Chat bubbles   │
              │  Sidebar history│
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   SQLite DB     │
              │  db.py          │
              │  chat_history.db│
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ LangGraph Graph │
              │  workflow.py    │
              └────────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────▼───────┐
│   Rewrite   │ │  Retriever  │ │  Response   │
│   Agent     │ │   Agent     │ │   Agent     │
│ agents.py   │ │  agents.py  │ │  agents.py  │
└─────────────┘ └──────┬──────┘ └─────────────┘
                       │
              ┌────────▼────────┐
              │    ChromaDB     │
              │  chroma_db/     │
              │  HuggingFace    │
              │  Embeddings     │
              └─────────────────┘
```

---

## Project Structure

```
.
├── app.py              # Streamlit chat UI
├── agents.py           # Rewrite, retriever, and response agents
├── workflow.py         # LangGraph pipeline (3-node graph)
├── state.py            # Shared TypedDict state
├── prompt.py           # System prompts and prompt builders
├── db.py               # SQLite conversation history
├── notebook.ipynb      # Document ingestion notebook
│
├── chroma_db/          # Vector database (auto-generated)
├── chat_history.db     # SQLite database (auto-generated)
├── .env.example        # API key template
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Quickstart

### Prerequisites

- Python 3.10+
- A Groq API key (free at [console.groq.com](https://console.groq.com)) or Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/your-username/medical-rag-assistant.git
cd medical-rag-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY="your_key_here"
```

### 4. Ingest your document

Open `notebook.ipynb` and run all cells. This loads the PDF, splits it into chunks, strips metadata, and stores the clean text in ChromaDB.

> **Re-run this whenever you change the PDF.**
> Delete `chroma_db/` first to avoid duplicate entries.

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Database Schema

Conversation history is stored in a local SQLite file (`chat_history.db`):

```sql
CREATE TABLE messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT,       -- unique UUID per conversation
    role        TEXT,       -- 'user' or 'assistant'
    content     TEXT,       -- message text
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

| Function | Description |
|---|---|
| `init_db()` | Creates the table if it doesn't exist |
| `create_session()` | Generates a new UUID for a new conversation |
| `save_message()` | Saves a single message to the database |
| `load_messages()` | Loads all messages for a given session |
| `get_all_sessions()` | Returns all past sessions with first message preview |

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Orchestration | LangGraph | Stateful multi-agent graph with typed state |
| LLM | Groq (Llama 3.3 70B) | Fast inference, generous free tier |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Free, runs locally, good semantic quality |
| Vector DB | ChromaDB | Lightweight, local, no extra setup |
| Conversation DB | SQLite | Built into Python, zero config, persistent |
| UI | Streamlit | Rapid chat UI with custom CSS theming |
| PDF Loading | PyMuPDF | Fast PDF parsing with clean text extraction |
| Config | python-dotenv | Simple `.env` file management |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key for LLM inference |

---

## Design Decisions

**Why query rewriting?**
User questions are often short and vague — "what causes it?" doesn't retrieve well. The rewrite agent reformulates the question into a full, specific sentence before searching, which improves retrieval accuracy significantly.

**Why strip metadata before storing in ChromaDB?**
LangChain's PDF loader attaches heavy metadata to every chunk — file path, producer, creation date, author, etc. This metadata gets passed to the LLM with every retrieved chunk, wasting ~200 tokens per chunk. Stripping it at ingestion time saves ~1,000 tokens per query (with k=5).

**Why trim chat history to 4 messages?**
Sending the full conversation history to the LLM on every query grows token usage quickly. The last 4 messages (2 turns) give enough context for follow-up questions without bloating the prompt.

**Why SQLite over session state for history?**
`st.session_state` is wiped every time the browser tab is closed or the app restarts. SQLite persists to disk, so conversations survive restarts and are available across sessions — like a real chat app.
