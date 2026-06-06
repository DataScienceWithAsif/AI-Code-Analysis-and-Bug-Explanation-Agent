import os
from groq import Groq
from state import AgentState
from prompts.templates import BUG_PROMPT

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def detect_bug(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    prompt = BUG_PROMPT + "\n\nInput:\n" + user_input

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You detect bugs in code."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()

    bug_type = "Unknown"
    location = "Unknown"
    # Changed from 'content' to keep the UI clean
    root_cause = "Unknown" 

    for line in content.splitlines():
        low = line.lower()
        # Added safe checks to ensure the colon exists before splitting
        if low.startswith("bug type") and ":" in line:
            bug_type = line.split(":", 1)[1].strip()
        elif low.startswith("location") and ":" in line:
            location = line.split(":", 1)[1].strip()
        elif low.startswith("root cause") and ":" in line:
            root_cause = line.split(":", 1)[1].strip()

    # Fallback: If parsing completely failed, dump the raw response into root_cause
    if root_cause == "Unknown":
        root_cause = content

    return {
        **state,
        "bug_type": bug_type,
        "bug_location": location,
        "root_cause": root_cause,
    }