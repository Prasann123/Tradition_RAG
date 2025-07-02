from langgraph.graph import StateGraph, END
from backend.agents.web_agent import web_agent
from backend.schema import AgentState
from backend.supervisor import supervisor
from backend.agents.rag_agent import rag_agent
from backend.agents.llm_agent import llm_agent
from backend.agents.decision_agent import validator_agent

def build_agent_graph():
    """"Build the state for multi agent system"""

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("rag", rag_agent)
    graph.add_node("web", web_agent)
    graph.add_node("llm", llm_agent)  
    graph.add_node("validator",validator_agent)

    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        lambda state: state.next_agent,
        {
            "rag": "rag",
            "web": "web",
            "llm": "llm"
        }
    )     
    
    graph.add_edge("rag", "llm")
    graph.add_edge("web", "llm")
  
    graph.add_edge("llm", "validator")

    graph.add_conditional_edges(
        "validator",
        # The lambda function checks the validation_result in the state
        lambda state: "supervisor" if state.is_valid is False else END,
        {
            "supervisor": "supervisor",
            END: END
        }
    )
    

    return graph.compile()


    


if __name__ == '__main__':
    graph = build_agent_graph()
    
    # Get the underlying graphviz graph object
    graph_viz = graph.get_graph()
    
    # Draw the graph to a PNG file
    image_bytes = graph_viz.draw_mermaid_png()
    
    # Save the image to your project directory
    with open("agent_graph.png", "wb") as f:
        f.write(image_bytes)
        
    print("Graph visualization saved to agent_graph.png")