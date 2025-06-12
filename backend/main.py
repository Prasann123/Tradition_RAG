import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Fix the import statement to use relative imports
# This will work when running as a module with python -m backend.main
from backend.api import chat_bp, document_bp, web_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
    
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(document_bp, url_prefix='/api')
    app.register_blueprint(web_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)