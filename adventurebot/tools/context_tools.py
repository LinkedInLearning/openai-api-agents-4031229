from agents import RunContextWrapper, function_tool
from ..models import TripContext, CHILD_AGE_THRESHOLD # Import constant

@function_tool
async def update_child_threshold_status(context: RunContextWrapper[TripContext]) -> str:
    """
    Checks participant ages in the context and updates the meets_child_threshold flag.

    Args:
        context: The run context containing the TripContext.
    """
    if not context.context or not context.context.query:
        return "Error: Trip query context not found."

    participant_ages = context.context.query.participant_ages
    meets_threshold = any(age < CHILD_AGE_THRESHOLD for age in participant_ages)
    context.context.meets_child_threshold = meets_threshold

    status = "met" if meets_threshold else "not met"
    return f"Child age threshold ({CHILD_AGE_THRESHOLD}) status updated: {status}."
