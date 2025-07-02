from schema import AgentState
from graph import build_agent_graph


def test_graph():
    graph = build_agent_graph()
    initial_state = AgentState(query="Just testing the graph flow")
    final_state = graph.invoke(initial_state)
    print("Final state:", final_state)

if __name__ == "__main__":
    test_graph()