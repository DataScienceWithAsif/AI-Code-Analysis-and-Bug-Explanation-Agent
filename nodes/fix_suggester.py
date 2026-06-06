from groq import Groq
from state import AgentState
from prompts.templates import FIX_PROMPT
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def suggest_fix(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    bug_type = state.get("bug_type", "Unknown")
    root_cause = state.get("root_cause", "")
    prompt = f"""{FIX_PROMPT}

Bug Type: {bug_type}
Root Cause: {root_cause}

User input:
{user_input}
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You write corrected code and explain fixes."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()

    return {
        **state,
        "fix_code": content,
        "fix_explanation": content,
    }