# AdventureBot

AdventureBot is a demonstration project that uses the OpenAI Agents SDK to plan personalized trips. It showcases how to build multi-agent systems using the Agents SDK.

## Project Structure

- `main.py` - Entry point for the application
- `models.py` - Data models for trip inputs
- `manager.py` - Orchestrates the agent workflow
- `printer.py` - Handles progress display
- `agents/` - Directory containing agent definitions
  - `weather_agent.py` - Gets weather information for trip dates
  - `search_plan_agent.py` - Plans search queries for activities
  - `search_agent.py` - Searches for activities using planned queries
  - `evaluation_agent.py` - Evaluates activities for group suitability
  - `recommender_agent.py` - Creates final recommendations

## Workflow

1. The user provides trip details (dates, location, participants)
2. The weather agent gets forecasts for the trip dates
3. The search plan agent creates a strategy for finding activities
4. The search agent executes queries to find activities
5. The evaluation agent scores activities for the group
6. The recommender agent creates the final trip recommendations

## Running the Project

```bash
# From project root
python -m adventurebot.main
```

## Extending the Project

This project is designed to be simple and extensible. You can:

- Add new agent types in the `agents` directory
- Enhance the recommendation logic
- Add user interaction to collect real trip data
- Connect to real weather APIs

## SDK Features Demonstrated

- Agent creation and configuration
- Structured outputs using Pydantic models
- Running agents with the Runner
- Asynchronous parallel execution
- Tracing and observation

This project serves as a learning tool for the OpenAI Agents SDK, focusing on simplicity and readability.
