from agents import Runner, trace, gen_trace_id, Agent
from agents.result import RunResult
from .models import TripQuery, TripContext
from .agents import (
    create_weather_agent, WeatherAnalysis,
    create_recommendation_agent, TripPlan,
)


class AdventureManager:
    """Manages the simplified adventure planning workflow with custom tool examples."""

    def __init__(self):
        self.recommendation_agent: Agent[TripContext] = create_recommendation_agent()

    async def run(self, query: TripQuery) -> None:
        """Run the simplified adventure planning workflow"""
        trace_id = gen_trace_id()
        print(f"Starting adventure planning... (Trace ID: {trace_id})")
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

        # Create the context object
        trip_context = TripContext(query=query)

        with trace("Adventure Planning (Simplified)", trace_id=trace_id):
            # 1. Get Weather Information
            weather_info = await self._get_weather_info(trip_context)

            # 2. Generate Trip Plan (includes evaluation and recommendations)
            trip_plan = await self._generate_trip_plan(weather_info, trip_context)

            # Display the final trip plan
            self._print_trip_plan(trip_plan)

    async def _get_weather_info(self, context: TripContext) -> WeatherAnalysis:
        """Run the WeatherAgent to get weather information."""
        print("Fetching weather information...")

        input_str = (
            f"Get weather analysis for a trip to {context.query.location} "
            f"from {context.query.start_date} to {context.query.end_date}."
        )

        result = await Runner.run(
            self.weather_agent,
            input_str,
            context=context
        )

        weather_info = result.final_output_as(WeatherAnalysis)
        print("Weather information fetched.")
        return weather_info

    async def _generate_trip_plan(
        self,
        weather_info: WeatherAnalysis,
        context: TripContext
    ) -> TripPlan:
        """Run the RecommendationAgent to evaluate activities and create the final plan."""
        print("Evaluating activities and creating trip plan...")

        # Prepare input string including all necessary context
        participants_str = f"{context.query.participant_number} participants (ages: {context.query.participant_ages})"
        dates_str = f"{context.query.start_date} to {context.query.end_date}"
        input_str = (
            f"Create a trip plan for {context.query.location} from {dates_str} "
            f"for {participants_str}.\n\n"
            f"Weather Information:\n{weather_info.model_dump()}\n\n"
        )

        result = await Runner.run(
            self.recommendation_agent,
            input_str,
            context=context
        )

        trip_plan = result.final_output_as(TripPlan)
        print("Trip plan generated.")
        return trip_plan

    def _print_trip_plan(self, plan: TripPlan) -> None:
        """Print the final trip plan in a structured format."""
        print("\n=== Your Adventure Plan ===\n")
        print(f"Location: {plan.location}")
        print(f"Dates: {plan.dates}")
        print(f"Participants: {plan.participants_summary}\n")
        
        print(f"Weather Summary:\n{plan.weather_summary}\n")

        print("Recommended Activities:")
        if not plan.recommended_activities:
            print("- No specific activities recommended based on search and evaluation.")
        for activity in plan.recommended_activities:
            print(f"\n- {activity.name}")
            print(f"  Description: {activity.description}")
            print(f"  Reasoning: {activity.reasoning}")
            if activity.best_time:
                print(f"  Best Time: {activity.best_time}")
            if activity.source_url:
                print(f"  More Info: {activity.source_url}")
            if activity.weather_considerations:
                print("  Weather Considerations:")
                for consideration in activity.weather_considerations:
                    print(f"    - {consideration}")
            if activity.preparation_tips:
                print("  Preparation Tips:")
                for tip in activity.preparation_tips:
                    print(f"    - {tip}")
        
        print("\nPacking List:")
        if not plan.packing_list:
            print("- No specific packing items suggested.")
        for item in plan.packing_list:
            print(f"- {item}")

        print("\nGeneral Tips:")
        if not plan.general_tips:
            print("- No general tips provided.")
        for tip in plan.general_tips:
            print(f"- {tip}")
