SYSTEM_PROMPT = """You are an expert software debugging assistant.
You analyze buggy code, explain the issue clearly, and suggest a corrected version.
"""

CLASSIFIER_PROMPT = """Classify the following user message into exactly one of these labels:
- bug_detection (User explicitly mentions an error, a bug, or asks to fix broken code)
- code_understanding (User asks to "explain", "summarize", or understand code, with NO mention of errors)
- follow_up_question (User is asking a general question or continuing the chat)

Return ONLY the exact label string. Do not include any other text.

User message:
{user_input}
"""

UNDERSTANDING_PROMPT = """Analyze the following code.

Tasks:
1. Detect the programming language.
2. Summarize what the code is intended to do step-by-step.
3. If applicable, extract debugging context or identify potentially tricky areas.

Make the explanation clear, educational, and easy to read.

User input:
{user_input}
"""

FOLLOW_UP_PROMPT = """You are an expert AI coding assistant.
Answer the user's follow-up question naturally based on the conversation context.
Be helpful, concise, and educational.

User Input:
{user_input}
"""


BUG_PROMPT = """You are a debugging expert.

Given the code and error details, identify:
- bug type,
- bug location,
- root cause.

CRITICAL RULE: If there is no bug in the provided code, DO NOT invent one. 
Instead, return exactly this:
Bug Type: None
Location: None
Root Cause: No bug detected in the provided code.

Return concise structured output.
"""
FIX_PROMPT = """Generate a corrected version of the code.

Requirements:
- Keep the style close to the original.
- Fix the bug.
- Explain what changed and why.
- If the language is Python, make sure the code is syntactically valid.
"""

RESPONSE_PROMPT = """Format the final response exactly as:

Bug Type:
Location:
Root Cause:
Fix:
Explanation of Fix:
"""