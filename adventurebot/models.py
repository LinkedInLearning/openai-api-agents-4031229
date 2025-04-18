from typing import List, Optional  # Added Optional
from pydantic import BaseModel, Field

# Define shared constants
CHILD_AGE_THRESHOLD = 12


class TripQuery(BaseModel):
    """Input data structure for adventure planning"""
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    location: str
    participant_number: int
    participant_ages: List[int]


class TripContext(BaseModel):
    """Context object holding trip details and derived information."""
    query: TripQuery
    meets_child_threshold: bool = Field(default=False, description="Flag indicating if any participant meets the child age threshold.")


# --- Moved Models ---

class ActivityResult(BaseModel):
    """Structured result of an activity search"""
    name: str
    description: str
    location: str
    age_range: Optional[List[int]] = None  # [min_age, max_age] if applicable
    price_range: Optional[str] = None
    duration: Optional[str] = None
    weather_dependent: bool
    source_url: Optional[str] = None


class SearchResult(BaseModel):
    """Collection of activities found from search"""
    activities: List[ActivityResult]
    search_summary: str