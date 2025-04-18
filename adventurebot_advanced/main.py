import asyncio

from .manager import AdventureManager
from .models import TripQuery


async def main() -> None:
    """
    Main entry point for the AdventureBot application.
    Creates a sample trip query and runs the adventure planning process.
    """
    # Sample trip query data
    query = TripQuery(
        start_date="2025-04-18",
        end_date="2025-04-21",
        location="Bowen Island, British Columbia",
        participant_number=5,
        participant_ages=[47, 47, 40, 40, 8]
    )
    
    # Initialize and run the adventure manager
    await AdventureManager().run(query)


if __name__ == "__main__":
    asyncio.run(main())
