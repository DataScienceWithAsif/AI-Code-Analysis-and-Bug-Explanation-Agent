from groq import Groq
from state import AgentState
from prompts.templates import UNDERSTANDING_PROMPT
from utils.helpers import detect_language
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def understand_code(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    language_guess = detect_language(user_input)
    prompt = UNDERSTANDING_PROMPT.format(user_input=user_input)

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You analyze source code and debugging context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()

    return {
        **state,
        "language": language_guess,
        "code": user_input,
        "intent": content,
    }