from typing import TypedDict, Optional

class AgentState(TypedDict, total=False):
    user_input: str
    chat_history: str    # ADD THIS
    task_type: str
    
    # Bug Pipeline
    bug_type: str
    bug_location: str
    root_cause: str
    fix_code: str
    fix_explanation: str
    
    # Understanding Pipeline
    language: str
    code: str
    intent: str
    
    # Follow-up Pipeline
    final_response: str  # ADD THIS