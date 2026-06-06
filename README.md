# AI Code Analysis and Bug Explanation Agent

An AI-powered debugging and tutoring assistant built with **LangGraph**, **Groq**, **Streamlit**, and **SQLite persistence**. 

This system acts as an intelligent coding tutor. It accepts user input, classifies the intent, and dynamically routes the request to either hunt down a bug, explain complex code block-by-block, or answer conversational follow-up questions using short-term memory.

---

## Project Overview

Debugging and understanding code are some of the most time-consuming tasks in software development. This project helps students, junior developers, and educators interact with code through a conversational AI agent.

The agent follows a dynamic, multi-stage workflow:

1. **Task Classification & Memory Injection:** Determines if the user is reporting a bug, asking for an explanation, or asking a follow-up question based on the current context.
2. **Dynamic Routing:** * **Bug Pipeline:** Analyzes code, detects the bug type, finds the location, suggests a fix, and explains the solution.
    * **Understanding Pipeline:** Analyzes working code and provides a step-by-step educational summary.
    * **Conversational Pipeline:** Acts as a general AI tutor, answering questions based on the chat history.
3. **Response Generation:** Streams real-time structured output or conversational text to the Streamlit UI.

---

## Key Features

* **Dynamic LangGraph Workflow:** Conditional edges route prompts to specialized LLM nodes based on user intent.
* **Conversational Memory:** Passes recent chat history into the graph state, allowing the AI to answer contextual follow-up questions (e.g., "Why did you use a dictionary instead of a list?").
* **Live Token Streaming:** Bug reports are streamed live to the UI for a highly responsive feel.
* **Advanced Session Management:** Dual SQLite databases track user sessions in the UI while LangGraph maintains internal state checkpoints.
* **Interactive Sidebar:** Users can seamlessly generate new threads, load historical conversations, and fully delete old chats.
* **Fail-Safe Parsing:** Custom Python logic prevents the application from crashing if the LLM hallucinates formatting.

---

## Technology Stack

* **Python 3.11**
* **Streamlit** (Frontend UI)
* **LangGraph** (Agentic State Machine & Routing)
* **langgraph-checkpoint-sqlite** (State Persistence)
* **Groq API** (Llama-3.3-70b-versatile for fast LLM inference)
* **SQLite3** (Custom UI metadata tracking)
* **python-dotenv**

---

## Project Structure

```text
bug_explanation_agent/
├── app.py                     # Main Streamlit UI and dynamic rendering logic
├── graph.py                   # LangGraph state machine and conditional routing
├── state.py                   # TypedDict defining the agent's memory payload
├── requirements.txt
├── .env.example
├── README.md
├── data/                      # Auto-generated SQLite databases
│   ├── conversations.db       # UI sidebar tracking
│   └── langgraph_checkpoints.db # LangGraph internal memory
├── prompts/
│   └── templates.py           # System prompts for all LLM nodes
├── nodes/
│   ├── classifier.py          # Determines user intent
│   ├── understanding.py       # Code summarization logic
│   ├── bug_detector.py        # Identifies bug type and root cause
│   ├── fix_suggester.py       # Writes corrected code
│   ├── follow_up_handler.py   # Handles contextual chat queries
│   └── response_generator.py  # Streams formatted bug reports
├── memory/
│   └── sqlite_memory.py       # DB connection and session management logic
└── utils/
    └── helpers.py             # Utility functions (e.g., language detection)