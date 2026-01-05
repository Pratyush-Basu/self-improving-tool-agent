from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import agent_node, tool_node, summary_node, evaluate_node, learn_node

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("summary", summary_node)
    workflow.add_node("evaluate", evaluate_node)
    workflow.add_node("learn", learn_node)
    
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", "tool")
    workflow.add_edge("tool", "summary")
    workflow.add_edge("summary", "evaluate")
    workflow.add_edge("evaluate", "learn")
    workflow.add_edge("learn", END)
    
    return workflow.compile()

graph = create_graph()