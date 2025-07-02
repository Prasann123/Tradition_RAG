from flask import Blueprint, request, jsonify
from backend.graph import build_agent_graph
from backend.schema import AgentState
from queue import Queue
import threading
import asyncio


agent_bp = Blueprint('agent', __name__)

agent_graph = build_agent_graph()

def run_agent_in_thread(graph, initial_state, result_queue):
    """Runs the async agent and puts the result in a queue."""
    try:
        # This is the blocking call, now safely in a background thread
        final_state = asyncio.run(graph.ainvoke(initial_state))
        result_queue.put(final_state)
    except Exception as e:
        result_queue.put({"error": str(e)})

@agent_bp.route("/invoke_agent", methods=["POST"])
def invoke_agent():
    data = request.get_json()
    query = data.get("query", "")
    config = data.get("config", {})
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    initial_state = AgentState(
        query=query,
        config=config,
        next_agent="supervisor"  # Start with the supervisor agent
    )
    result_queue = Queue()
    thread = threading.Thread(
        target=run_agent_in_thread,
        args=(agent_graph, initial_state.dict(), result_queue)
    )
    thread.start()
    final_state = result_queue.get()
    if "error" in final_state:
        return jsonify({"error": f"Agent execution failed: {final_state['error']}"}), 500

   # final_state = asyncio.run(agent_graph.ainvoke(initial_state))
    return jsonify({
        "final_answer": final_state.get("final_answer", ""),
        "feedback": final_state.get("feedback", ""),
        "is_valid": final_state.get("is_valid"),
        "sources": final_state.get("sources", []),
        "answer_source": final_state.get("answer_source")
    }), 200