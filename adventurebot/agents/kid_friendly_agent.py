from typing import List, Optional
from pydantic import BaseModel

from agents import Agent, WebSearchTool
from ..models import TripContext, SearchResult  # Import SearchResult from ..models

PROMPT = """You are a specialized search agent focused on finding activities suitable for children.
        
        Given the trip details (location, dates, participant ages including children) and weather information:
        1. Focus your web search on activities explicitly marked as kid-friendly, family-oriented, or suitable for the specific ages of the children involved.
        2. Look for parks, playgrounds, interactive museums, age-appropriate workshops, family-friendly restaurants, etc.
        3. Execute searches using the web search tool.
        4. For each promising activity found, extract and structure key information:
           - Name and description (highlighting child-friendly aspects)
           - Location
           - Specific age appropriateness (e.g., "best for ages 5-10")
           - Price range (mentioning child/family discounts if found)
           - Duration
           - Weather dependency
           - Source URL
        5. Compile a list of structured ActivityResult objects (defined within the SearchResult model).
        6. Provide a concise summary focusing on the suitability for the children in the group.
        
        Return the results in the SearchResult format. You MUST use the web search tool."""


def create_kid_friendly_activity_agent() -> Agent[TripContext]:  
    """Create an agent specialized in finding kid-friendly activities."""
    return Agent[TripContext](  
        name="Kid-Friendly Activity Agent",
        instructions=PROMPT,
        output_type=SearchResult,
        tools=[WebSearchTool()],
    )
