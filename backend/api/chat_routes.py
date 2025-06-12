from flask import Blueprint, request, jsonify
from backend.services.chat_service import process_message

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    message = data['message']
    search_type_str = data.get('search_type', 'knnBeta')
   
    result = process_message(message,search_type_str)
    
    return jsonify({"answer": result})