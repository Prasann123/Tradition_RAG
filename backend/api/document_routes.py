from flask import Blueprint, request, jsonify
from backend.utils.enums import IndexMechanism
import os
import asyncio
from backend.services.document_service import extract_topics_from_documents
from backend.services.document_service import list_documents
from backend.services.document_service import (
    process_file, 
    process_video,
    process_text
)

document_bp = Blueprint('document', __name__)

@document_bp.route('/upload-file', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Get index mechanism from query param or default to FLAT
    index_mech_str = request.args.get("index_mech", "FLAT")
    try:
        index_mech = IndexMechanism[index_mech_str.upper()]
    except KeyError:
        return jsonify({"error": f"Invalid index_mech '{index_mech_str}'. Valid options: {[e.name for e in IndexMechanism]}"}), 400

    # Process file
    result = asyncio.run(process_file(file, index_mech=index_mech.value))
    return jsonify({"answer": result})

@document_bp.route('/upload-video', methods=['POST'])
def upload_video_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No video selected"}), 400
    
    # Process video
    result = asyncio.run(process_video(file))
    return jsonify({"answer": result})

@document_bp.route('/upload-text', methods=['POST'])
def upload_text_route():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    # Get index mechanism from query param or default to FLAT
    index_mech = request.args.get("index_mech", "FLAT")
    # Process text
    result = asyncio.run(process_text(data['text'], index_mech=index_mech))
    return jsonify({"answer": result})

@document_bp.route('/list_documents', methods=['GET'])
def list_documents_route():
    documents = asyncio.run(list_documents())
    return jsonify({"documents": documents})

@document_bp.route('/list_topics', methods=['GET'])
def list_topics_route():
    """
    Returns a list of topics/keywords extracted from the stored documents.
    Optional query param: limit (default 20)
    """
    limit = int(request.args.get("limit", 20))
    topics = asyncio.run(extract_topics_from_documents(limit=limit))
    return jsonify({"topics": topics})