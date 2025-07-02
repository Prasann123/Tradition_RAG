from backend.tools.base_tools import TravelTool
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
import os
import re

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class BudgetCalculatorTool(TravelTool):
    """Tool for planning budget for attractive destinations.  """
    async def execute(self, state):
        destination = state.query.get("destination")
        currency =  state.query.get("currency")
     
        flight_onward_price = state.flight_onward_prices
        flight_return_price = state.flight_return_prices

        nights = state.query.get("nights", 3)
        budget = {}
        search =TavilySearchResults(api_key=TAVILY_API_KEY)
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        queries = {
                    "hotel": f"average price per night for a 3-star hotel room (not hostel) in the city center of {destination} in {currency}",
                    "restaurant": f"average total daily cost for three meals (breakfast, lunch, dinner) per person at mid-range restaurants in {destination} in {currency}",
                    "attraction": f"average total daily cost of visiting two popular attractions per person in {destination} in {currency}",
                    "transportation": f"average daily cost of public transportation (bus, metro, taxi) per person in {destination} in {currency}"
                }
        # 1st let us try in tavily search
        for key, query in queries.items():
            try:
                result = await search.run(query)
                # Extract the first $number found in the result
                match = re.search(r"(\d{1,6}(?:\.\d{1,2})?)\s?(USD|INR|EUR|₹|\$)?", result, re.IGNORECASE)
                if match:
                    budget[key] = float(match.group(1))
                else:
                    budget[key] = None
            except Exception as e:
                budget[key] = None

            # if tavily does not produce results search in llm
        missing = [k for k, v in budget.items() if v is None]  
        for k in missing:               
            prompt = f"What is the average {k} price in {destination} in {currency}?"
            llm_response =  llm.invoke(prompt)
            llm_result = llm_response.content if hasattr(llm_response, "content") else llm_response
            match = re.search(r"(\d{1,6}(?:\.\d{1,2})?)\s?(USD|INR|EUR|₹|\$)?", llm_result, re.IGNORECASE)
            if match:
                budget[k] = int(match.group(1))
            else:
                budget[k] = None
            # finally if both reults fails use the default values
        fallback_values = {"hotel": 100, "restaurant": 40, "attraction": 20, "transportation": 15}
        for k in budget:
            if budget[k] is None:
                budget[k] = fallback_values[k]

        hotel_total = budget["hotel"] * nights
        restaurant_total = budget["restaurant"] * nights
        attraction_total = budget["attraction"] * nights
        transportation_total = budget["transportation"] * nights
        flight_total = flight_onward_price + flight_return_price
        total_budget = flight_total + hotel_total + restaurant_total + attraction_total + transportation_total

        state.budget_breakdown = {
            "hotel": hotel_total,
            "restaurants": restaurant_total,
            "attractions": attraction_total,
            "transportation": transportation_total,         
            "flight_total": flight_total
        }    
        state.total_budget = total_budget
        state.messages.append({
            "role": "tool",
            "tool_name": "BudgetCalculatorTool",
            "content": (
                 f"Estimated total budget: {total_budget} (hotel: {hotel_total}, restaurants: {restaurant_total}, "
                f"attractions: {attraction_total}, transportation: {transportation_total}, "
                f"flight onward: {flight_onward_price}, flight return: {flight_return_price})"
            )
        })


        return state