from langgraph.graph import StateGraph, END
from backend.travel_supervisor import travel_Supervisor
from langgraph.checkpoint.memory import MemorySaver
from backend.state_schema.travel_planner_schema import TravelPlannerState
from backend.main import travel_planner
import uuid


def build_agent_graph():
    """"Build the state for travel agent system"""
    memory = MemorySaver()
    thread_id = str(uuid.uuid4())

    graph = StateGraph(TravelPlannerState)

    graph.add_node("supervisor", travel_Supervisor)
    graph.add_node("tools", travel_planner.plan)


    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        lambda state: "tools" if state.next_agent == "tools" else END,
        {
            "tools": "tools",
            END: END,
        }
    )
    # After tools, always go back to supervisor
    graph.add_edge("tools", "supervisor")
    graph.add_edge("supervisor", END)
    

    return graph.compile()    


if __name__ == '__main__':
    graph = build_agent_graph()
    
    # Get the underlying graphviz graph object
    graph_viz = graph.get_graph()
    
    # Draw the graph to a PNG file
    image_bytes = graph_viz.draw_mermaid_png()
    
    # Save the image to your project directory
    with open("travel_agent_graph.png", "wb") as f:
        f.write(image_bytes)
        
    print("Graph visualization saved to travel_agent_graph.png")