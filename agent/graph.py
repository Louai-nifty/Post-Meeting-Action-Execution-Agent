from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.extraction_node import extraction_node

def route_after_extraction(state: AgentState) -> str:
    if state.status == "extraction_failed":
        return END
    return "next_node"

workflow = StateGraph(AgentState)

workflow.add_node("extraction", extraction_node)
workflow.add_node("next_node", next_node)

workflow.set_entry_point("extraction")

workflow.add_conditional_edges(
    "extraction",
    route_after_extraction,
    {
        END: END,
        "next_node": "next_node",
    }
)

graph = workflow
