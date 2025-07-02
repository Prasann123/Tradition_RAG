from flask import Blueprint, request, jsonify
from backend.utils.enums import IndexMechanism
from werkzeug.utils import secure_filename
import os
import asyncio
from backend.services.document_service import extract_topics_from_documents
from backend.services.document_service import list_documents
from backend.services.document_service import (
    process_file, 
    process_text
)
import uuid
import threading

UPLOAD_FOLDER = 'uploads'
document_bp = Blueprint('document', __name__)
upload_statuses = {}

@document_bp.route('/upload-file', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    config = request.form.to_dict()
    job_id = str(uuid.uuid4())
    upload_statuses[job_id] = {"status": "pending", "message": "Upload received, job is starting."}
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    # Process file
    thread = threading.Thread(target=asyncio.run, args=(process_file(filepath, config, job_id, upload_statuses),))
    thread.start()
    return jsonify({"message": "File upload started.", "job_id": job_id}), 202

@document_bp.route('/upload-status/<job_id>', methods=['GET'])
def get_upload_status(job_id):
    """Endpoint for the UI to poll for progress updates."""
    status = upload_statuses.get(job_id, {"status": "not_found", "message": "Job ID not found."})
    return jsonify(status)

@document_bp.route('/upload-text', methods=['POST'])
def upload_text_route():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text_content = data.get("text")
    config = data.get("config", {})
    result = asyncio.run(process_text(text_content, config=config))
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