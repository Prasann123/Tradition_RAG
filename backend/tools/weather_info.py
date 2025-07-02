from backend.tools.base_tools import TravelTool
import os
import httpx
from collections import Counter
from datetime import datetime, timedelta

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_ENDPOINT = os.getenv("OPEN_WEATHER_ENDPOINT")


class WeatherInfoTool(TravelTool):
    """Tool for getting weather infor of destination.  """
    async def execute(self, state):
        destination = state.query.get("destination")
        nights = state.query.get("nights", 3)
        target_date = state.query.get("start_date") 
        start_date = datetime.strptime(target_date, "%Y-%m-%d")
        date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(nights)]
        params = {
              "q": destination,
              "appid": OPEN_WEATHER_API_KEY,
              "units":"metric"
        }
        try:
              async with httpx.AsyncClient() as client:
                    response = await client.get(OPEN_WEATHER_ENDPOINT,params=params)
                    response.raise_for_status()
                    data =  response.json()
                    summaries=[]
                    for date in date_list:
                        forecasts = [entry for entry in data.get("list", []) if entry["dt_txt"].startswith(date)]
                        if forecasts:
                          temps = [f["main"]["temp"] for f in forecasts]
                          descriptions = [f["weather"][0]["description"] for f in forecasts]
                          avg_temp = sum(temps) / len(temps)
                          common_desc = Counter(descriptions).most_common(1)[0][0]
                          summaries.append(f"{date}: {common_desc}, avg temp {avg_temp:.1f}°C")
                        else:
                          summaries.append(f"{date}: No weather data available.")
                    state.weather = "Weather forecast:\n" + "\n".join(summaries)      
                    state.messages.append({
                          "role": "tool",
                          "tool_name": "weatherinfotool",
                          "content": f"Weather for {destination}: {state.weather}"
                    })        
        except Exception as e:
              state.weather = "Error retrieving weather information: " + str(e)
              state.messages.append({
                    "role": "tool",
                    "tool_name": "weatherinfotool",
                    "content": f"Error retrieving weather information for {destination}: {str(e)}"
              })
              

        return state