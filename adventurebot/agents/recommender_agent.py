from typing import List, Optional
from pydantic import BaseModel

from agents import Agent
from ..models import TripContext 

PROMPT = """You evaluate potential activities and create a final travel plan.
        
        Given the list of potential activities (ActivityResults), the weather analysis (WeatherAnalysis), and the original trip query details (location, dates, participants):
        1. Evaluate each activity based on:
           - Suitability for the participant ages.
           - Appropriateness considering the weather summary.
           - Group enjoyment potential (can everyone participate?).
           - Practical considerations (cost, duration, accessibility inferred from description).
        2. Select the top 3-5 activities that best fit the group and conditions.
        3. For each selected activity, create a detailed recommendation (ActivityRecommendation):
           - Include a clear reasoning for why it's a good fit.
           - Suggest the best time/day if possible.
           - List weather considerations and preparation tips.
           - Preserve the source URL.
        4. Summarize the key weather information.
        5. Generate a suggested packing list based on weather and activities.
        6. Add general travel tips relevant to the location or type of trip.
        7. Compile everything into the final TripPlan format.
        
        Focus on creating a practical, enjoyable, and well-reasoned plan for the specific group."""

class ActivityRecommendation(BaseModel):
    """Detailed activity recommendation based on evaluation"""
    name: str
    description: str
    reasoning: str # Why this activity is recommended for the group
    best_time: Optional[str] = None
    weather_considerations: List[str]
    preparation_tips: List[str]
    source_url: Optional[str] = None


class TripPlan(BaseModel):
    """Complete evaluated trip plan with recommendations"""
    location: str
    dates: str # e.g., "YYYY-MM-DD to YYYY-MM-DD"
    participants_summary: str # e.g., "2 adults, 1 child (age 8)"
    weather_summary: str
    recommended_activities: List[ActivityRecommendation]
    packing_list: List[str]
    general_tips: List[str]


def create_recommendation_agent() -> Agent[TripContext]:  
    """Create an agent that evaluates activities and generates final trip recommendations."""
    return Agent[TripContext]( 
        name="Recommendation Agent",
        instructions=PROMPT,
        output_type=TripPlan,
    )