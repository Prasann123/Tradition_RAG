# Export the blueprints so they can be imported directly from the api package
from .chat_routes import chat_bp
from .document_routes import document_bp

from .agent_routes import agent_bp
from .travelsgent_routes import travel_agent_bp

# Define what's available when someone does "from api import *"
__all__ = ['chat_bp', 'document_bp', 'agent_bp', 'travel_agent_bp']