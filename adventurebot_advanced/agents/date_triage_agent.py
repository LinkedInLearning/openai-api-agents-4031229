from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from agents import Agent


class DateAnalysis(BaseModel):
    """Analysis of date range relative to current date"""
    is_within_10_days: bool
    start_month: str
    end_month: str
    days_until_start: int


def create_date_triage_agent() -> Agent:
    """Create an agent specialized in date range analysis"""
    return Agent(
        name="Date Triage Agent",
        instructions="""You analyze trip dates and route to appropriate agents based on timing.
        
        1. Compare the date range with the current date:
           - Calculate days until trip start
           - Determine if within 10 days
           - Extract months for longer-term forecasts
        
        2. Route based on timing:
           - If within 10 days: Use the transfer_to_weather_analyst tool
           - If beyond 10 days: Use the transfer_to_weather_search_agent tool
        
        Always provide structured analysis output AND use the appropriate handoff tool.""",
        output_type=DateAnalysis
    )