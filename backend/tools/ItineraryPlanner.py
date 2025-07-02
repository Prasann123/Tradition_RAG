from backend.tools.base_tools import TravelTool


class ItineraryPlannerTool(TravelTool):
    """ tool for planning the itinerary for attractions planned"""

    async def execute(self,state):
        
        nights = state.query.get("nights", 3)
        attractions = getattr(state, "attractions", [])
        restaurants = getattr(state, "restaurants", [])
        hotels = getattr(state, "hotels", [])
        transportation = getattr(state, "transportation", [])
        itinerary = []


        for day in range(nights):
            day_plan={
                "day": day + 1,
                "hotel": hotels[0] if hotels else "No hotel found",
                "attractions": attractions[day::nights] if attractions else [],
                "restaurant": restaurants[day % len(restaurants)] if restaurants else "No restaurant found",
                "transportation": transportation[day % len(transportation)] if transportation else "No transportation info"
            }
            itinerary.append(day_plan)
        state.itinerary = itinerary
        state.messages.append({
            "role": "tool",
            "tool_name": "ItineraryPlannerTool",
            "content": f"Itinerary planned for {nights} nights",
            "result": itinerary
        })
        return state
            