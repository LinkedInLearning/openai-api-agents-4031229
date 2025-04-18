from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from agents import Agent, WebSearchTool
from ..models import TripContext 

PROMPT = f"""You are a weather analyst that helps travelers prepare for their trip.
        The current date is {datetime.now().date()}.

        1. Determine if the trip start date is within 10 days from the current date.
        2. If the trip is within 10 days: Provide a specific (simulated) forecast including temperature range, precipitation chance, clothing recommendations, and any warnings.
        3. If the trip is more than 10 days away: 
           - Use the web search tool to find historical weather patterns and climate information for the location and month(s) of the trip.
           - Provide general recommendations based on historical averages/typical conditions (temperature range, precipitation chance, clothing).
           - Do not specify a year, just the month and location for the search.
        4. Return a structured analysis using the WeatherAnalysis format.
        
        Always use the web search tool if the trip is more than 10 days away."""

class WeatherAnalysis(BaseModel):
    """Weather analysis with recommendations"""
    summary: str
    temperature_range: List[float]  # [min_temp, max_temp]
    precipitation_chance: float
    recommended_clothing: List[str]
    weather_warnings: Optional[List[str]] = None


def create_weather_agent() -> Agent[TripContext]:  
    """Create a weather analysis agent that provides weather information for a trip.
    
    It uses web search for dates more than 10 days in the future and provides
    general recommendations based on historical data for those cases.
    For dates within 10 days, it provides a more specific forecast (simulated).
    """
    return Agent[TripContext](  
        name="Weather Agent",
        instructions=PROMPT,
        output_type=WeatherAnalysis,
        tools=[WebSearchTool()],
    )