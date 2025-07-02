import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Fix the import statement to use relative imports
# This will work when running as a module with python -m backend.main

from backend.tools.attraction_search import AttractionSearchTool
from backend.tools.weather_info import WeatherInfoTool
from backend.tools.budget_calculator import BudgetCalculatorTool
from backend.tools.currency_converter import CurrencyConvertorhTool
from backend.tools.ItineraryPlanner import ItineraryPlannerTool
from backend.planner.travel_planner import TravelPlanner
from backend.tools.FlightSearch import FlightSearchTool

# Load environment variables
load_dotenv()

tools_list = [
            AttractionSearchTool(),
            FlightSearchTool(),
            WeatherInfoTool(),
            CurrencyConvertorhTool(),
            BudgetCalculatorTool(),           
            ItineraryPlannerTool(),
            ]
travel_planner = TravelPlanner(tools_list)

def create_app():
    from backend.api.chat_routes import chat_bp
    from backend.api.document_routes import document_bp
    from backend.api.agent_routes import agent_bp
    from backend.api.travelsgent_routes import travel_agent_bp
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
    
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(document_bp, url_prefix='/api')
    app.register_blueprint(agent_bp, url_prefix='/api')
    app.register_blueprint(travel_agent_bp, url_prefix='/api') 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)