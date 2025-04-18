from typing import Optional, List
from pydantic import BaseModel

from agents import Agent


class WeatherAnalysis(BaseModel):
    """Weather analysis with recommendations"""
    summary: str
    temperature_range: List[float]  # [min_temp, max_temp]
    precipitation_chance: float
    recommended_clothing: List[str]
    weather_warnings: Optional[List[str]] = None


def create_weather_agent() -> Agent:
    """Create a weather analysis agent that provides weather information for a trip"""
    return Agent(
        name="Weather Agent",
        instructions="""You are a weather analyst that helps travelers prepare for their trip.
        
        1. Use available weather data sources to determine weather conditions
        2. Analyze the forecast and provide practical recommendations
        3. Include specific clothing and gear recommendations
        4. Note any weather-related warnings or concerns
        
        Return a structured analysis with temperature ranges, precipitation chances, 
        and practical advice for the specific location and dates.""",
        output_type=WeatherAnalysis,
    )