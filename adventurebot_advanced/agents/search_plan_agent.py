from typing import List
from pydantic import BaseModel

from agents import Agent


class SearchQuery(BaseModel):
    """A structured search query with context"""
    query: str
    reason: str
    priority: int  # 1-5, with 1 being highest priority


class SearchPlan(BaseModel):
    """Collection of search queries for activity research"""
    queries: List[SearchQuery]
    location_context: str


def create_search_plan_agent() -> Agent:
    """Create an agent that plans search queries for trip activities"""
    return Agent(
        name="Search Planner",
        instructions="""You create a strategic plan of search queries to find trip activities.
        
        Based on the trip details (location, dates, participant ages, and weather):
        1. Create 3-5 specific search queries that would find good activities
        2. For each query, explain why it's relevant to the trip
        3. Include a mix of:
           - General activities in the location
           - Age-appropriate activities for the group
           - Seasonal or weather-dependent options
           - Local recommendations
        4. Assign a priority to each query (1-5, with 1 being highest priority)
        
        Return a structured plan with your search queries and the location context.""",
        output_type=SearchPlan
    )