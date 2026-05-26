import sqlite3

def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role      TEXT,
            content   TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

def save_message(session_id, role, content):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    conn.commit()
    conn.close()


def load_messages(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"role": row[0], "content": row[1]} for row in rows]

# session id
import uuid

def create_session():
    return str(uuid.uuid4())

#function to get all past sessions so the user can go back to them

def get_all_sessions():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT session_id, MIN(timestamp), MIN(content)
        FROM messages
        GROUP BY session_id
        ORDER BY MIN(timestamp) DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [{"session_id": row[0], "started_at": row[1], "first_message": row[2]} for row in rows]