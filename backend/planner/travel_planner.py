from backend.tools.base_tools import TravelTool
from backend.state_schema.travel_planner_schema import TravelPlannerState

class TravelPlanner:
    def __init__(self,tools: list[TravelTool]):
        self.tools = tools

    async def plan(self, state:TravelPlannerState) -> TravelPlannerState:
        """Executes the travel planning process using the provided tools."""
        for tool in self.tools:
            state = await tool.execute(state)
        return state