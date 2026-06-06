from groq import Groq
from state import AgentState
from prompts.templates import FOLLOW_UP_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def handle_follow_up(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    chat_history = state.get("chat_history", "")
    
    prompt = FOLLOW_UP_PROMPT.format(user_input=user_input)

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant. Use the chat history to provide accurate answers."},
            # Inject the chat history directly into the system/context messages
            {"role": "user", "content": f"Chat History:\n{chat_history}"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = resp.choices[0].message.content.strip()
    
    return {**state, "final_response": content}