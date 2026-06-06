import os
from groq import Groq
from state import AgentState
from prompts.templates import RESPONSE_PROMPT

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def build_final_prompt(state: AgentState) -> str:
    return f"""{RESPONSE_PROMPT}

Bug Type: {state.get("bug_type", "Unknown")}
Location: {state.get("bug_location", "Unknown")}
Root Cause: {state.get("root_cause", "Unknown")}
Fix Code:
{state.get("fix_code", "")}
Explanation:
{state.get("fix_explanation", "")}
"""

def stream_response_text(state: AgentState):
    prompt = build_final_prompt(state)

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You format debugging explanations clearly and accurately."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        stream=True,
    )

    final_text = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            final_text += delta
            yield delta

    state["final_answer"] = final_text