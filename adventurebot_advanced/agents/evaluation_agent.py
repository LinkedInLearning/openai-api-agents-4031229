from typing import List, Optional
from pydantic import BaseModel

from agents import Agent


class AgeScore(BaseModel):
    """Score for a specific age"""
    age: int
    score: float  # 0-10


class ActivityEvaluation(BaseModel):
    """Detailed evaluation of an activity"""
    activity_name: str
    overall_score: float  # 0-10
    age_scores: List[AgeScore]
    group_enjoyment_score: float  # 0-10
    considerations: List[str]
    source_url: Optional[str] = None


class EvaluationResult(BaseModel):
    """Complete evaluation of all activities"""
    evaluations: List[ActivityEvaluation]
    group_recommendations: List[str]
    overall_summary: str


def create_evaluation_agent() -> Agent:
    """Create an agent that evaluates activities for group suitability"""
    return Agent(
        name="Evaluation Agent",
        instructions="""You evaluate activities for how well they suit a group of travelers.
        
        For each activity:
        1. Score it overall from 0-10
        2. Score how appropriate it is for each age in the group (0-10)
        3. Calculate a group enjoyment score based on how well it works for everyone
        4. List important considerations (accessibility, difficulty, etc.)
        5. Preserve the source URL
        
        Then provide overall recommendations for the group and a summary.
        Focus on finding activities that everyone in the group can enjoy together.""",
        output_type=EvaluationResult
    )