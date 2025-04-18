"""Agent definitions for the AdventureBot application"""

from agents import Agent, Runner, trace, gen_trace_id

from .weather_agent import create_weather_agent, WeatherAnalysis
from .search_plan_agent import create_search_plan_agent, SearchPlan, SearchQuery
from .search_agent import create_search_agent, SearchResult, ActivityResult
from .evaluation_agent import create_evaluation_agent, EvaluationResult, ActivityEvaluation
from .recommender_agent import create_recommender_agent, TripRecommendations, ActivityRecommendation

__all__ = [
    # Agent creation functions
    'create_weather_agent',
    'create_search_plan_agent',
    'create_search_agent',
    'create_evaluation_agent', 
    'create_recommender_agent',
    
    # Model types
    'WeatherAnalysis',
    'SearchPlan',
    'SearchQuery',
    'SearchResult',
    'ActivityResult',
    'EvaluationResult',
    'ActivityEvaluation',
    'TripRecommendations',
    'ActivityRecommendation',
    
    # SDK re-exports
    'Agent',
    'Runner',
    'trace',
    'gen_trace_id'
]