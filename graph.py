from langgraph.graph import StateGraph, END
from state import ResearchState
from agents.planner import planner_agent
from agents.searcher import searcher_agent
from agents.writer import writer_agent
from agents.critic import critic_agent

def build_graph():
    # Create the graph with our state schema
    graph = StateGraph(ResearchState)

    # Add all agent nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("searcher", searcher_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("critic", critic_agent)

    # Define the flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "writer")
    graph.add_edge("writer", "critic")

    # Conditional edge: critic can send back to writer or end
    def should_revise(state):
        # We do max 1 revision — critic always ends after one pass
        return END

    graph.add_conditional_edges("critic", should_revise)

    return graph.compile()

# Build once, reuse
research_graph = build_graph()
