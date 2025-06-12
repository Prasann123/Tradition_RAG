from flask import Blueprint, request, jsonify
from backend.services.web_service import scrape_website_content

web_bp = Blueprint('web', __name__)

@web_bp.route('/scrape-website', methods=['POST'])
def scrape_website_route():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url = data['url']
    result = scrape_website_content(url)
    
    return jsonify({"answer": result})