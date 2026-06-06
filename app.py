import streamlit as st
from dotenv import load_dotenv
from graph import build_graph
from memory.sqlite_memory import init_db, get_thread_id, list_conversations, touch_thread, delete_conversation, create_new_thread
from nodes.response_generator import stream_response_text

# Initialize environment and database
load_dotenv()
init_db()

# Streamlit Page Config
st.set_page_config(page_title="AI Bug Explanation Agent", page_icon="🐞", layout="wide")
st.title("AI Code Analysis and Bug Explanation Agent")
st.caption("LangGraph + Groq + SQLite persistence + True live token streaming")

# Build the LangGraph agent
graph = build_graph()

# Ensure we have an active thread_id in the session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = get_thread_id()

thread_id = st.session_state.thread_id

# Ensure chat history exists in session state for the UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR LOGIC ---
with st.sidebar:
    st.header("Session")
    st.write(f"Active Thread: `{thread_id}`")

    # New Conversation Button
    # New Conversation Button
    if st.button("➕ New conversation", use_container_width=True):
        create_new_thread() # Force generate and save the new ID
        st.session_state.messages = [] # Clear the UI
        st.rerun()

    st.divider()
    st.subheader("Saved Conversations")
    
    conversations = list_conversations()
    
    if not conversations:
        st.caption("No saved conversations yet.")
    else:
        for conv in conversations:
            t_id = conv['thread_id']
            
            # Create two columns: 80% for Load, 20% for Delete
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Button to load the conversation
                if st.button(f"📄 {t_id[:8]}...", key=f"load_{t_id}", help=f"Load {t_id}"):
                    st.session_state.thread_id = t_id
                    st.session_state.messages = [] # Clear UI to start fresh for this context
                    st.rerun()
            
            with col2:
                # Button to delete the conversation
                if st.button("🗑️", key=f"del_{t_id}", help="Delete"):
                    delete_conversation(t_id)
                    
                    # If they delete the active thread, reset to a new one
                    if st.session_state.thread_id == t_id:
                        create_new_thread() # Force generate a new active ID
                        st.session_state.messages = []
                    
                    st.rerun()

# --- MAIN CHAT UI ---
# Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
prompt = st.chat_input("Paste code, error message, or ask a follow-up question")

if prompt:
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Display Assistant Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        config = {"configurable": {"thread_id": thread_id}}

        # Extract the last 5 messages for context
        history_list = st.session_state.messages[-6:-1] 
        history_str = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in history_list])

        # Invoke the LangGraph agent WITH chat history
        result = graph.invoke({
            "user_input": prompt,
            "chat_history": history_str
        }, config=config)
        
        base_state = dict(result) if isinstance(result, dict) else {"user_input": prompt}

        streamed_text = ""
        task_type = base_state.get("task_type", "").strip().lower()

        # Route 1: Bug Detection (Use the streamer)
        if "bug_detection" in task_type:
            for token in stream_response_text(base_state):
                streamed_text += token
                placeholder.markdown(streamed_text)
                
        # Route 2: Code Understanding (Pull the 'intent' variable from understanding.py)
        elif "code_understanding" in task_type:
            streamed_text = base_state.get("intent", "Explanation generated but not found in state.")
            placeholder.markdown(streamed_text)
            
        # Route 3: Follow-up Questions (Pull the 'final_response' from follow_up_handler.py)
        elif "follow_up" in task_type:
            streamed_text = base_state.get("final_response", "Response generated but not found in state.")
            placeholder.markdown(streamed_text)
            
        # Fallback
        else:
            streamed_text = "No valid response could be generated from the agent state."
            placeholder.markdown(streamed_text)

    # 3. Save Assistant Message & Update DB
    st.session_state.messages.append({"role": "assistant", "content": streamed_text})
    touch_thread(thread_id)