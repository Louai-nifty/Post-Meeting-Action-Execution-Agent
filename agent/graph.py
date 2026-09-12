from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.extraction_node import extraction_node

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("extraction", extraction_node)

# Set entry point and edges
workflow.set_entry_point("extraction")
workflow.add_edge("extraction", END)

graph = workflow
