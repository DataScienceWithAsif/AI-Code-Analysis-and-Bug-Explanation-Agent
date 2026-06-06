from groq import Groq
from state import AgentState
from prompts.templates import CLASSIFIER_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=key)

def classify_task(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    chat_history = state.get("chat_history", "")
    
    # Prepend history so the classifier understands context
    contextual_input = f"PREVIOUS CHAT HISTORY:\n{chat_history}\n\nCURRENT USER MESSAGE:\n{user_input}"
    prompt = CLASSIFIER_PROMPT.format(user_input=contextual_input)

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You classify user intent based on the conversation context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    label = resp.choices[0].message.content.strip()
    return {**state, "task_type": label}