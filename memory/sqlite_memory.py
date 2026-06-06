import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

DB_PATH = Path("data/conversations.db")
LANGGRAPH_DB_PATH = Path("data/langgraph_checkpoints.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Tracking threads
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    # Tracking UI chat bubbles
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_new_thread():
    new_id = str(uuid.uuid4())[:8]
    st.session_state.thread_id = new_id
    conn = sqlite3.connect(DB_PATH)
    now = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT OR IGNORE INTO conversations VALUES (?, ?, ?)",
        (new_id, now, now),
    )
    conn.commit()
    conn.close()
    return new_id

def get_thread_id():
    if "thread_id" not in st.session_state:
        create_new_thread()
    return st.session_state.thread_id

def touch_thread(thread_id: str):
    conn = sqlite3.connect(DB_PATH)
    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE conversations SET updated_at=? WHERE thread_id=?",
        (now, thread_id),
    )
    conn.commit()
    conn.close()

def list_conversations():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT thread_id, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
    ).fetchall()
    conn.close()
    return [{"thread_id": r[0], "created_at": r[1], "updated_at": r[2]} for r in rows]

# --- NEW FUNCTIONS FOR UI MESSAGES ---
def save_message(thread_id: str, role: str, content: str):
    """Saves a single UI chat bubble to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO chat_messages (thread_id, role, content) VALUES (?, ?, ?)",
        (thread_id, role, content)
    )
    conn.commit()
    conn.close()

def get_messages(thread_id: str):
    """Retrieves all UI chat bubbles for a specific thread."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM chat_messages WHERE thread_id = ? ORDER BY id ASC",
        (thread_id,)
    ).fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]
# -----------------------------------

def delete_conversation(thread_id: str):
    conn1 = sqlite3.connect(DB_PATH)
    try:
        conn1.execute("DELETE FROM conversations WHERE thread_id = ?", (thread_id,))
        # Also delete the saved UI messages for this thread
        conn1.execute("DELETE FROM chat_messages WHERE thread_id = ?", (thread_id,))
        conn1.commit()
    except sqlite3.Error as e:
        print(f"Database error during UI tracking deletion: {e}")
    finally:
        conn1.close()
        
    if LANGGRAPH_DB_PATH.exists():
        conn2 = sqlite3.connect(LANGGRAPH_DB_PATH)
        try:
            conn2.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
            conn2.execute("DELETE FROM writes WHERE thread_id = ?", (thread_id,))
            conn2.commit()
        except sqlite3.Error as e:
            print(f"Database error during LangGraph deletion: {e}")
        finally:
            conn2.close()