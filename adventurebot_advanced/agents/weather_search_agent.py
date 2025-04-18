from typing import List, Optional
from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings


class WeatherAnalysis(BaseModel):
    """Weather analysis with recommendations found from a search"""
    summary: str
    temperature_range: List[float]  # [min_temp, max_temp]
    precipitation_chance: float
    recommended_clothing: List[str]
    weather_warnings: Optional[List[str]] = None


def create_weather_search_agent() -> Agent:
    """Create an agent specialized in weather search and analysis for dates beyond 10 days"""
    return Agent(
        name="Weather Search Agent",
        instructions="""You are a specialized search engine for historical weather analysis that helps travelers prepare for their trip.
        
        For dates beyond 10 days:
        1. Use web search to find historical weather patterns and climate information
        2. Focus on typical conditions for that month of the year
        3. Do not specify a year, just the month and location
        4. Provide general recommendations based on historical data
        5. Include average temperature ranges and precipitation chance
        
        Always consider the specific location and dates when making recommendations.""",
        output_type=WeatherAnalysis,
        tools=[WebSearchTool()],
        model_settings=ModelSettings(tool_choice="required"),
    )
