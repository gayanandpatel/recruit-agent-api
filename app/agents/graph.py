from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import extract_candidate_data, evaluate_match, critique_evaluation

def routing_logic(state: AgentState) -> str:
    # If fair, or if we've looped too many times (prevent infinite loops), end the graph.
    if state["critic_review"].is_fair or state["revision_count"] >= 2:
        return END
    return "evaluator"

# Initialize the state graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("extractor", extract_candidate_data)
workflow.add_node("evaluator", evaluate_match)
workflow.add_node("critic", critique_evaluation)

# Define edges
workflow.set_entry_point("extractor")
workflow.add_edge("extractor", "evaluator")
workflow.add_edge("evaluator", "critic")

# Add conditional routing from the critic
workflow.add_conditional_edges(
    "critic",
    routing_logic,
    {
        END: END,
        "evaluator": "evaluator"
    }
)

# Compile the graph
agent_executor = workflow.compile()