from backend.tools.base_tools import TravelTool
import os
import httpx

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GOOGLE_PLACES_ENDPOINT = os.getenv("GOOGLE_PLACES_ENDPOINT")

class AttractionSearchTool(TravelTool):
    """Tool for searching attractive destinations."""
    async def execute(self, state):
        destination = state.query.get("destination")
        start_date = state.query.get("start_date")
        categories = {
            "attractions": f"top tourist attractions in {destination} on {start_date}" if start_date else f"top tourist attractions in {destination}",
            "restaurants": f"restaurants in {destination}",
            "transportation": f"transportation in {destination}",
            "activities": f"things to do in {destination} on {start_date}" if start_date else f"things to do in {destination}",
            "hotels": f"hotels in {destination} on {start_date}" if start_date else f"hotels in {destination}"
        }
        results = {}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                for key, query in categories.items():
                    params = {
                        "query": query,
                        "key": GOOGLE_PLACES_API_KEY,
                        "type": key
                    }
                    response = await client.get(GOOGLE_PLACES_ENDPOINT, params=params)
                    response.raise_for_status()
                    data = response.json()
                    if data.get("status") != "OK":
                        results[key] = []
                    else:
                        places = data.get("results", [])
                        results[key] = [place.get("name") for place in places]

            # Assign results to state fields after the loop
            state.attractions = results.get("attractions", [])
            state.restaurants = results.get("restaurants", [])
            state.transportation = results.get("transportation", [])
            state.activities = results.get("activities", [])
            state.hotels = results.get("hotels", [])
            state.messages.append({
                "role": "tool",
                "tool_name": "AttractionSearchTool",
                "content": f"Found attractions for {destination}",
                "result": results
            })
        except Exception as e:
            state.attractions = []
            state.restaurants = []
            state.transportation = []
            state.activities = []
            state.hotels = []
            state.messages.append({
                "role": "tool",
                "tool_name": "AttractionSearchTool",
                "content": f"Error fetching attractions for {destination}: {str(e)}"
            })
        return state