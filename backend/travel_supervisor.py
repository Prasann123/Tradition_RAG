from backend.main import travel_planner
from langchain_openai import ChatOpenAI
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)


async def travel_Supervisor(state):
    SYSTEM_PROMPT = """
You are a helpful travel planning assistant. Your job is to help users plan trips by searching for attractions, activities, and destinations, providing weather forecasts, calculating total and daily budgets, and performing currency conversions as needed. Use the available tools to gather accurate information, perform calculations, and answer user questions clearly and concisely. Always explain your reasoning and cite sources when possible.
"""
    user_question = state.query
    input_text = f"{SYSTEM_PROMPT}\n\nUser question: {user_question}\n\n"
    state.messages.append({
    "role": "supervisor",
    "content": f"Supervisor invoked with query: {user_question}",
    "system_prompt": SYSTEM_PROMPT
})
    try:
        state = await travel_planner.plan(state)
        
        summary_prompt = f"""
You are a travel planning assistant. Here is the user's question:
{user_question}

You have access to the following tools and their results:
- AttractionSearchTool: {getattr(state, 'attractions', '')}
- RestaurantSearchTool: {getattr(state, 'restaurants', '')}
- HotelSearchTool: {getattr(state, 'hotels', '')}
- TransportationSearchTool: {getattr(state, 'transportation', '')}
- WeatherInfoTool: {getattr(state, 'weather', '')}
- BudgetCalculatorTool: {getattr(state, 'total_budget', '')}
- ItineraryPlannerTool: {getattr(state, 'itinerary', '')}
- CurrencyConvertorTool: {getattr(state, 'currency_conversion', '')}
- FlightSearchTool: Onward: {getattr(state, 'flights_onward', '')}, Return: {getattr(state, 'flights_return', '')}
- FlightPriceTool: Onward: {getattr(state, 'flight_onward_prices', '')}, Return: {getattr(state, 'flight_return_prices', '')}

Please summarize all this information into a clear, friendly, and actionable travel plan for the user. 
- Organize the summary by category (dates, flights, hotel, attractions, weather, budget, etc.).
- Use markdown formatting: bold section headings, bullet points for lists, and clear separation between sections.
- If any information is missing, mention it politely.
- End with a friendly closing or travel tip.
- When summarizing flights, highlight the cheapest options and recommend the best value considering both price and convenience (duration, layovers, etc.).
- Write for a traveler, not a developer.
"""
        summary =  llm.invoke(summary_prompt).content
        state.final_answer = summary
        state.messages.append({
            "role": "supervisor",
            "content": "Final summary generated for user.",
            "summary": summary
        })
        state.next_agent = "END"
    except Exception as e:
        state.final_answer = "An error occurred."
        state.next_agent = "END"
        state.messages.append({
            "role": "supervisor",
            "content": f"Error: {str(e)}"
        })

    return state
   
    
