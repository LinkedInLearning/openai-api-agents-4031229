from typing import List, Optional
from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings


class ActivityResult(BaseModel):
    """Structured result of an activity search"""
    name: str
    description: str
    location: str
    age_range: Optional[List[int]] = None  # [min_age, max_age] if applicable
    price_range: Optional[str] = None
    duration: Optional[str] = None
    weather_dependent: bool
    source_url: Optional[str] = None


class SearchResult(BaseModel):
    """Collection of activities found from a search"""
    activities: List[ActivityResult]
    search_summary: str


def create_search_agent() -> Agent:
    """Create an agent that searches for activities and returns structured results"""
    return Agent(
        name="Search Agent",
        instructions="""You are a search agent that finds activities and events for trip planning.
        
        For each search:
        1. Execute the web search query to find relevant activities
        2. Extract and structure key information for each activity:
           - Name and description
           - Location details
           - Age appropriateness
           - Price information (if available)
           - Duration information (if available)
           - Weather dependency
        3. Include the source URL for each activity
        4. Summarize the overall search findings
        
        Return a structured list of activities with a summary of what you found.""",
        output_type=SearchResult,
        tools=[WebSearchTool()],
        model_settings=ModelSettings(tool_choice="required"),
    )
