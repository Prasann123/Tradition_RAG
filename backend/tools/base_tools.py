from abc import ABC, abstractmethod
from backend.state_schema.travel_planner_schema import TravelPlannerState



class TravelTool(ABC):
    """abstract base class for travel tools"""
    @abstractmethod
    async def execute(self,state: TravelPlannerState) -> TravelPlannerState:
       pass

  