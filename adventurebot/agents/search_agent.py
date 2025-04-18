from agents import Agent, WebSearchTool
from ..models import TripContext, CHILD_AGE_THRESHOLD, ActivityResult, SearchResult  # Import models from ..models

PROMPT = f"""You research and find suitable activities for a trip based on provided details.

Given the trip details (location, dates, participant ages) and weather information:

1. **Check for young children:** Use the `update_child_threshold_status` tool to determine if any participant is under {CHILD_AGE_THRESHOLD} years old. If the tool indicates the threshold is met:**
    a. Internally brainstorm 3-5 relevant search queries focusing on general activities, age-appropriate options (all age groups including the children), weather suitability, and local experiences.
   b. Execute searches using the **WebSearchTool**.
   c. Extract and structure key information for each promising activity (Name, description, location, age range, price, duration, weather dependency, source URL).
   d. Compile a list of structured ActivityResult objects.
   e. Provide a concise summary of the search process and findings.
   f. Return the results in the SearchResult format. You MUST use the WebSearchTool.

2. **If no young children (threshold not met):**
   a. Internally brainstorm 3-5 relevant search queries focusing on general activities, age-appropriate options (for the adult/older group), weather suitability, and local experiences.
   b. Execute searches using the **WebSearchTool**.
   c. Extract and structure key information for each promising activity (Name, description, location, age range, price, duration, weather dependency, source URL).
   d. Compile a list of structured ActivityResult objects.
   e. Provide a concise summary of the search process and findings.
   f. Return the results in the SearchResult format. You MUST use the WebSearchTool.

**Important:** Prioritize the child threshold check using the dedicated tool before proceeding with general search."""


def create_activity_search_agent() -> Agent[TripContext]:
    """Create an agent that searches for activities, uses tools, and hands off based on context."""
    return Agent[TripContext](
        name="Activity Search Agent",
        instructions=PROMPT, 
        output_type=SearchResult,
        tools=[WebSearchTool(), update_child_threshold_status],
    )
