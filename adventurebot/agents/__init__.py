"""Agent definitions for the AdventureBot application"""

from agents import Agent, Runner, trace, gen_trace_id

# Import the consolidated agent creation functions and their output types
from .weather_agent import create_weather_agent, WeatherAnalysis
from .recommender_agent import create_recommendation_agent, TripPlan, ActivityRecommendation
from .kid_friendly_agent import create_kid_friendly_activity_agent

# Import models from the central models file
from ..models import SearchResult, ActivityResult

__all__ = [
    # Agent creation functions
    'create_weather_agent',
    'create_recommendation_agent',
    'create_kid_friendly_activity_agent',

    # Model types (consolidated)
    'WeatherAnalysis',
    'ActivityResult',
    'TripPlan',
    'ActivityRecommendation',

    # SDK re-exports
    'Agent',
    'Runner',
    'trace',
    'gen_trace_id'
]