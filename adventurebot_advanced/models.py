from typing import List
from pydantic import BaseModel


class TripQuery(BaseModel):
    """Input data structure for adventure planning"""
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    location: str
    participant_number: int
    participant_ages: List[int]