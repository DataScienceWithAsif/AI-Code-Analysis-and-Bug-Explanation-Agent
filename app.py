import streamlit as st
from dotenv import load_dotenv
from graph import build_graph
from memory.sqlite_memory import init_db, get_thread_id, list_conversations, touch_thread, delete_conversation, create_new_thread, save_message, get_messages
from nodes.response_generator import stream_response_text

# Initialize environment and database
load_dotenv()
init_db()

# --- 1. MODERN UI CONFIGURATION & CSS ---
st.set_page_config(page_title="AI Bug Explanation Agent", page_icon="🐞", layout="wide")

# Inject custom CSS for a sleek web app feel
st.markdown("""
<style>
    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Make buttons look modern with hover effects */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Style the main title area */
    .main-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    .main-subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
        font-size: 1.1em;
    }
    
    /* Style the chat input box */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Modern Hero Header
st.markdown("<h1 class='main-header'>🐞 AI Code Analysis Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Your intelligent, context-aware pair programmer and debugging tutor.</p>", unsafe_allow_html=True)
st.divider()

# Build the LangGraph agent
graph = build_graph()

# Ensure we have an active thread_id in the session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = get_thread_id()

thread_id = st.session_state.thread_id

# Ensure chat history exists in session state for the UI
if "messages" not in st.session_state:
    st.session_state.messages = get_messages(st.session_state.thread_id)

# --- 2. SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown("### ⚙️ Session Control")
    st.caption(f"Active Thread: `{thread_id}`")

    # New Conversation Button (Primary style)
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        create_new_thread() # Force generate and save the new ID
        st.session_state.messages = [] # Clear the UI
        st.rerun()

    st.divider()
    st.markdown("### 📂 Saved Conversations")
    
    conversations = list_conversations()
    
    if not conversations:
        st.info("No saved conversations yet.")
    else:
        for conv in conversations:
            t_id = conv['thread_id']
            
            # Create two columns: 80% for Load, 20% for Delete
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Button to load the conversation
                if st.button(f"📄 {t_id[:8]}...", key=f"load_{t_id}", help=f"Load thread {t_id}"):
                    st.session_state.thread_id = t_id
                    st.session_state.messages = get_messages(t_id) 
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

# --- 3. MAIN CHAT UI ---

# Modern Empty State Welcome Screen
if not st.session_state.messages:
    with st.container():
        st.info("👋 **Welcome! I am ready to help you write better code.**\n\n"
                "* **Got a Bug?** Paste your code and the error message.\n"
                "* **Need an Explanation?** Paste a snippet and ask me how it works.\n"
                "* **Follow-ups?** Just ask naturally! I remember our conversation.")

# Render existing messages with custom avatars
for msg in st.session_state.messages:
    # Set modern avatars
    avatar_icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# User Input
prompt = st.chat_input("Paste code, error message, or ask a follow-up question...")

if prompt:
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(thread_id, "user", prompt) # SAVE TO DB
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 2. Display Assistant Response
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        
        # Add a sleek loading spinner while waiting for the graph to route
        with st.spinner("Analyzing context..."):
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
    save_message(thread_id, "assistant", streamed_text) # SAVE TO DB
    touch_thread(thread_id)