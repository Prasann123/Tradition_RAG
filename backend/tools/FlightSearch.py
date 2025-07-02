import asyncio
from backend.tools.base_tools import TravelTool
import os
import re
from amadeus import Client, ResponseError
from forex_python.converter import CurrencyRates

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

def extract_float(price_str):
    # This will extract the first float number from the string
    match = re.search(r"(\d+(?:\.\d+)?)", str(price_str))
    return float(match.group(1)) if match else 0.0
class FlightSearchTool(TravelTool):
    """Tool for searching scheduled flights between two airports, including return, using Amadeus API."""
    async def execute(self, state):
        user_currency = state.query.get("currency", "EUR")
        currencyConvertor = CurrencyRates()
        exchange_rate = await asyncio.to_thread(currencyConvertor.get_rate, 'EUR', user_currency)
        origin = state.query.get("from")     
        destination = state.query.get("to")   
        date = state.query.get("start_date") 
        return_date = state.query.get("return_date")  
        n_persons = state.query.get("adults", 1)

        amadeus = Client(
            client_id=AMADEUS_API_KEY,
            client_secret=AMADEUS_API_SECRET
        )

        try:
            # Onward flights
            response_onward = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=date,
                adults=n_persons,
                max=5
            )
            flights_onward = response_onward.data
            flight_list_onward = []
            for flight in flights_onward:
                segments = flight['itineraries'][0]['segments']
                carrier = segments[0]['carrierCode']
                dep_time = segments[0]['departure']['at']
                arr_time = segments[-1]['arrival']['at']
                price_eur = extract_float(flight['price']['total'])
                price_currency = flight['price']['currency']
                if price_currency != user_currency:
                    converted_price = round(price_eur * exchange_rate, 2)
                    price_str = f"{converted_price} {user_currency} (converted from {price_eur} {price_currency})"
                else:
                    price_str = f"{price_eur} {price_currency}"
                flight_list_onward.append(
                     f"Carrier: {carrier}, Departs: {dep_time}, Arrives: {arr_time}, Price: {price_str}"
                )
            state.flight_onward_prices = extract_float(price_str)


            # Return flights (if return_date provided)
            flight_list_return = []
            if return_date:
                response_return = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=destination,
                    destinationLocationCode=origin,
                    departureDate=return_date,
                    adults=n_persons,
                    max=5
                )
                flights_return = response_return.data
                for flight in flights_return:
                    segments = flight['itineraries'][0]['segments']
                    carrier = segments[0]['carrierCode']
                    dep_time = segments[0]['departure']['at']
                    arr_time = segments[-1]['arrival']['at']
                    price_eur = extract_float(flight['price']['total'])
                    price_currency = flight['price']['currency']
                    if price_currency != user_currency:
                        converted_price = round(price_eur * exchange_rate, 2)
                        price_str = f"{converted_price} {user_currency} (converted from {price_eur} {price_currency})"
                    else:
                        price_str = f"{price_eur} {price_currency}"
                    flight_list_return.append(
                        f"Carrier: {carrier}, Departs: {dep_time}, Arrives: {arr_time}, Price: {price_str}"
                        )

            # Store in state
            state.flights_onward = flight_list_onward
            state.flights_return = flight_list_return
            state.flight_return_prices = extract_float(price_str)
            state.messages.append({
                "role": "tool",
                "tool_name": "FlightSearchTool",
                "content": f"Flights from {origin} to {destination} on {date}" +
                           (f" and return on {return_date}" if return_date else ""),
                "result": {
                    "onward": flight_list_onward,
                    "return": flight_list_return
                }
            })
        except ResponseError as e:
            state.flights_onward = []
            state.flights_return = []
            state.messages.append({
                "role": "tool",
                "tool_name": "FlightSearchTool",
                "content": f"Error fetching flights: {str(e)}"
            })
        return state