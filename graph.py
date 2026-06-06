from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from state import AgentState
from nodes.classifier import classify_task
from nodes.understanding import understand_code
from nodes.bug_detector import detect_bug
from nodes.fix_suggester import suggest_fix
from nodes.follow_up_handler import handle_follow_up # Import the new node

def route_initial_task(state: AgentState):
    """Routes based on the initial classifier output."""
    task_type = state.get("task_type", "").strip().lower()
    
    if "follow_up_question" in task_type:
        return "handle_follow_up"
    
    # Both bug detection and code understanding start at the understanding node
    return "code_understanding"

def route_after_understanding(state: AgentState):
    """Decides whether to stop at understanding or proceed to bug detection."""
    task_type = state.get("task_type", "").strip().lower()
    
    if "code_understanding" in task_type:
        return END # Stop the graph here; the user just wanted an explanation
    
    # Otherwise, proceed down the bug hunting pipeline
    return "bug_detection"

def build_graph():
    builder = StateGraph(AgentState)

    # 1. Add all nodes
    builder.add_node("task_classifier", classify_task)
    builder.add_node("code_understanding", understand_code)
    builder.add_node("bug_detection", detect_bug)
    builder.add_node("fix_suggestion", suggest_fix)
    builder.add_node("handle_follow_up", handle_follow_up)

    # 2. Start node
    builder.add_edge(START, "task_classifier")

    # 3. First Routing: Classifier -> Understanding OR Follow-up
    builder.add_conditional_edges(
        "task_classifier", 
        route_initial_task,
        {
            "code_understanding": "code_understanding",
            "handle_follow_up": "handle_follow_up"
        }
    )

    # 4. Second Routing: Understanding -> Bug Detection OR End
    builder.add_conditional_edges(
        "code_understanding",
        route_after_understanding,
        {
            END: END,
            "bug_detection": "bug_detection"
        }
    )

    # 5. Finish the bug detection pipeline
    builder.add_edge("bug_detection", "fix_suggestion")
    builder.add_edge("fix_suggestion", END)

    # 6. Finish the follow-up pipeline
    builder.add_edge("handle_follow_up", END)

    # Memory Persistence
    conn = sqlite3.connect("data/langgraph_checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    
    return builder.compile(checkpointer=checkpointer)