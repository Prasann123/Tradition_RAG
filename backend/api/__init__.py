# Export the blueprints so they can be imported directly from the api package
from .chat_routes import chat_bp
from .document_routes import document_bp
from .web_routes import web_bp

# Define what's available when someone does "from api import *"
__all__ = ['chat_bp', 'document_bp', 'web_bp']