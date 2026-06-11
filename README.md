# 🐞 AI Code Analysis & Bug Explanation Agent

<p align="center">
  <strong>Modern Streamlit + LangGraph assistant for code understanding, bug detection, and guided fixes.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="LangGraph" src="https://img.shields.io/badge/Orchestration-LangGraph-121D33">
  <img alt="LLM" src="https://img.shields.io/badge/LLM-Groq%20(Llama%203.3%2070B)-00A67E">
  <img alt="Persistence" src="https://img.shields.io/badge/Memory-SQLite-003B57?logo=sqlite&logoColor=white">
</p>

---

## ✨ What This Repository Does

This project is an AI coding assistant that helps you:

- **Detect and explain bugs** in pasted code + error context.
- **Understand working code** with educational, step-by-step explanations.
- **Ask follow-up questions** inside the same chat thread with memory-aware responses.

It uses a **LangGraph routing workflow** to classify user intent and send requests to specialized nodes.

---

## 🧠 Core Features

- **Intent Classification + Dynamic Routing**
  - `bug_detection`
  - `code_understanding`
  - `follow_up_question`
- **Structured Debugging Output** (bug type, location, root cause, fix, explanation)
- **Live Streaming Responses** for bug-report formatting
- **Conversation Memory** using SQLite-backed thread/message history
- **Persistent LangGraph Checkpoints** for agent state continuity
- **Modern Streamlit UI** with session sidebar controls

---

## 🏗️ Architecture Overview

```text
User Prompt
   │
   ▼
Task Classifier
   ├── follow_up_question ──► Follow-up Handler ──► End
   └── code_understanding/bug_detection
             ▼
      Code Understanding
         ├── code_understanding ──► End
         └── bug_detection
                  ▼
             Bug Detector
                  ▼
             Fix Suggester
                  ▼
                 End
```

---

## 📁 Project Structure

```text
AI-Code-Analysis-and-Bug-Explanation-Agent/
├── app.py                        # Streamlit app UI + interaction loop
├── graph.py                      # LangGraph nodes and routing logic
├── state.py                      # Shared state schema (AgentState)
├── requirements.txt              # Python dependencies
├── README.md
├── nodes/
│   ├── classifier.py             # Intent classification
│   ├── understanding.py          # Code explanation stage
│   ├── bug_detector.py           # Bug type/location/root cause extraction
│   ├── fix_suggester.py          # Fix generation
│   ├── follow_up_handler.py      # Context-aware Q&A replies
│   └── response_generator.py     # Streaming final response formatter
├── prompts/
│   └── templates.py              # Prompt templates for all stages
├── memory/
│   └── sqlite_memory.py          # Conversation/session persistence layer
└── utils/
    └── helpers.py                # Language detection + formatting helpers
```

> `data/` databases are auto-created at runtime and ignored by Git.

---

## ⚙️ Prerequisites

- Python **3.11+**
- A valid **Groq API key**

---

## 🚀 Quick Start

### 1) Clone and enter the project

```bash
git clone https://github.com/DataScienceWithAsif/AI-Code-Analysis-and-Bug-Explanation-Agent.git
cd AI-Code-Analysis-and-Bug-Explanation-Agent
```

### 2) Create and activate a virtual environment

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5) Run the app

```bash
streamlit run app.py
```

---

## 🧪 How to Use

Inside the chat input, you can do the following:

1. **Bug Detection Mode**
   - Paste buggy code and (optionally) error messages/logs.
   - The assistant returns: **Bug Type, Location, Root Cause, Fix, Explanation**.

2. **Code Understanding Mode**
   - Paste valid code and ask for explanation/summarization.
   - The assistant returns an educational, step-by-step breakdown.

3. **Follow-up Q&A Mode**
   - Ask contextual follow-up questions in the same thread.
   - The assistant uses recent chat history for continuity.

---

## 🖥️ UI Walkthrough

- **Main panel:** chat conversation with role-based avatars and streaming output.
- **Sidebar controls:**
  - Create new thread
  - Load previous thread
  - Delete thread
- **Persistence:**
  - `data/conversations.db` for UI sessions and messages
  - `data/langgraph_checkpoints.db` for LangGraph checkpoints

### Screenshots

<img width="1338" height="621" alt="AI agent UI screenshot 1" src="https://github.com/user-attachments/assets/4989973f-27d5-48af-b87c-7b89a431dbea" />
<img width="1356" height="618" alt="AI agent UI screenshot 2" src="https://github.com/user-attachments/assets/6e022195-9ce1-4ad7-ae0d-dfc934596aad" />

---

## 🔐 Security & Configuration Notes

- Never commit your `.env` file.
- This repo ignores `.env` and `data/` by default.
- Model calls use Groq API credentials from environment variables.

---

## 🛠️ Troubleshooting

- **Missing API key / auth errors:** verify `GROQ_API_KEY` in `.env`.
- **`ModuleNotFoundError`:** ensure virtualenv is active, then reinstall requirements.
- **Streamlit not launching:** run `streamlit run app.py` from the repository root.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Open a pull request.

---

## 📌 Summary

If you need an assistant that can **analyze code, explain bugs clearly, and keep context across follow-up questions**, this project gives you a complete local workflow with a clean Streamlit experience.
