from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TravelPlannerState(BaseModel):
    """Represents the shared state of the travel planner agent system."""
    
    # user inputs

    query: Dict[str, Any]= Field( description="User's travel-related query or input text")
    config: dict[str,Any] = Field(description="Configuration for the travel planner run", default_factory=dict)
    next_agent: str = Field(default="supervisor", description="Next agent pointer in the workflow")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Conversation and tool memory")

# outputs

    final_answer:str = Field(description="Final travel plan or answer after processing", default="")
    sources: list = Field(description="List of sources or documents used to generate the final answer", default_factory=list)
    answer_source :str = Field(description="The agent that was the source for the final answer", default="")
    feedback: Optional[str] = Field(default=None, description="Feedback or additional information from the agents")
    is_valid: Optional[bool] = Field(default=None, description="Indicates if the final")

# tool specific info

    itinerary: list = Field(default_factory=list, description="List of planned itinerary items")
    hotels: list = Field(default_factory=list, description="List of hotels or accommodations")
    attractions: list = Field(default_factory=list, description="List of attractions or points of interest")
    weather: str = Field(default="", description="Weather information for the travel destination")
    total_budget: float = Field(default=0.0, description="Total budget for the trip")
    currency_conversion: str = Field(default="USD", description="Currency conversion information")
    exchange_rate: float = Field(default=1.0, description="Exchange rate for currency conversion")
    restaurants: list = Field(default_factory=list, description="List of recommended restaurants")
    transportation: list = Field(default_factory=list, description="List of transportation options")
    activities: list = Field(default_factory=list, description="List of planned activities or events")
    budget_breakdown: dict = Field(default_factory=dict, description="Detailed breakdown of the travel budget")
    flights_onward: list = Field(default_factory=list, description="List of flight options or bookings")
    flights_return: list = Field(default_factory=list, description="List of return flight options or bookings")
    flight_onward_prices: float = Field(default_factory=float, description="Flight prices for different routes")
    flight_return_prices: float = Field(default_factory=float, description="Return flight prices for different routes")