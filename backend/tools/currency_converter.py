from backend.tools.base_tools import TravelTool
from forex_python.converter import CurrencyRates
import asyncio

class CurrencyConvertorhTool(TravelTool):
    """Tool for Currency Conversion tool for attractive destinations.  """
    async def execute(self, state):
        currency = state.query.get("currency")
        currencyConvertor = CurrencyRates()
        rate = await asyncio.to_thread(currencyConvertor.get_rate, 'USD', currency)
        state.exchange_rate = rate
        state.currency_conversion = f"1 USD = {rate} {currency}"
        state.messages.append({
            "role": "tool",
            "tool_name": "CurrencyConvertorhTool",
            "content": f"Currency conversion rate for {currency} is {rate}",
            "result": state.currency_conversion
        })
        return state