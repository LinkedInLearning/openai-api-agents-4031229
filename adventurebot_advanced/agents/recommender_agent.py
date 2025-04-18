from typing import List, Optional
from pydantic import BaseModel

from agents import Agent


class ActivityRecommendation(BaseModel):
    """Detailed activity recommendation"""
    name: str
    description: str
    best_time: str
    weather_considerations: List[str]
    preparation_tips: List[str]
    group_notes: str
    source_url: Optional[str] = None


class TripRecommendations(BaseModel):
    """Complete trip recommendations"""
    weather_summary: str
    recommended_activities: List[ActivityRecommendation]
    daily_schedule_suggestions: List[str]
    packing_list: List[str]
    general_tips: List[str]


def create_recommender_agent() -> Agent:
    """Create an agent that generates final trip recommendations"""
    return Agent(
        name="Recommender Agent",
        instructions="""You create comprehensive travel recommendations for a group trip.
        
        Based on the weather information and evaluated activities:
        1. Summarize the expected weather and its impact on the trip
        2. Recommend the best activities for the group with:
           - Practical timing suggestions
           - Weather considerations
           - Preparation tips
           - Special notes for the group
        3. Suggest a daily schedule that considers weather and group dynamics
        4. Create a packing list appropriate for the activities and weather
        5. Include general travel tips for the destination
        
        Make sure to preserve the source URLs from activities and focus on practical
        recommendations that help the group have an enjoyable trip.""",
        output_type=TripRecommendations
    )