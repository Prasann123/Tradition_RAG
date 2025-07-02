import uuid
from flask import Blueprint, request, jsonify
from backend.travel_planner_graph import build_agent_graph

travel_agent_bp = Blueprint('travel_agent_bp', __name__)
graph = build_agent_graph()

@travel_agent_bp.route('/travelsgent', methods=['POST'])
async def travelsgent():
    user_input = request.get_json()
    state = {
        "query": user_input.get("query"),
      
    }
    thread_id = str(uuid.uuid4())
    result = await graph.ainvoke(state)
    return jsonify({
        "final_answer": result.get("final_answer", ""),
        "thread_id": thread_id,
        "messages": result.get("messages", [])
    })