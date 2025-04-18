from __future__ import annotations

import asyncio
from typing import List

from rich.console import Console

from agents import Agent, Runner, trace, gen_trace_id
from .printer import Printer
from .models import TripQuery
from .agents import (
    create_weather_agent, WeatherAnalysis,
    create_search_plan_agent, SearchPlan,
    create_search_agent, SearchResult,
    create_evaluation_agent, EvaluationResult,
    create_recommender_agent, TripRecommendations
)


class AdventureManager:
    """Manages the adventure planning workflow using agents"""
    
    def __init__(self):
        self.console = Console()
        self.printer = Printer(self.console)
        
        # Create agents once during initialization
        self.weather_agent = create_weather_agent()
        self.search_plan_agent = create_search_plan_agent()
        self.search_agent = create_search_agent()
        self.evaluation_agent = create_evaluation_agent()
        self.recommender_agent = create_recommender_agent()

    async def run(self, query: TripQuery) -> None:
        """Run the adventure planning workflow"""
        trace_id = gen_trace_id()
        with trace("Adventure Planning", trace_id=trace_id):
            # Display trace ID for user reference
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )
            
            # 1. Get weather information
            weather_info = await self._get_weather_info(query)
            
            # 2. Plan searches based on location, dates, and weather
            search_plan = await self._plan_searches(query, weather_info)
            
            # 3. Execute searches in parallel
            search_results = await self._execute_searches(search_plan)
            
            # 4. Evaluate activities based on participant information
            evaluated_activities = await self._evaluate_activities(search_results, query)
            
            # 5. Generate final recommendations
            recommendations = await self._generate_recommendations(evaluated_activities, weather_info, query)
            
            # End the printer progress display
            self.printer.end()
            
            # Display recommendations to the user
            self._print_recommendations(recommendations)

    async def _get_weather_info(self, query: TripQuery) -> WeatherAnalysis:
        """Get weather information for the trip dates and location"""
        self.printer.update_item("weather", "Checking weather conditions...")
        
        input_str = (
            f"Check weather for {query.location} between "
            f"{query.start_date} and {query.end_date}"
        )
        
        result = await Runner.run(
            self.weather_agent,
            input_str
        )
        
        self.printer.mark_item_done("weather")
        return result.final_output_as(WeatherAnalysis)

    async def _plan_searches(self, query: TripQuery, weather_info: WeatherAnalysis) -> SearchPlan:
        """Plan search queries based on trip details and weather"""
        self.printer.update_item("planning", "Planning activity searches...")
        
        input_str = (
            f"Plan activity searches for trip to {query.location} "
            f"from {query.start_date} to {query.end_date} "
            f"for {query.participant_number} participants (ages: {query.participant_ages}).\n\n"
            f"Weather conditions to consider:\n{weather_info.model_dump()}"
        )
        
        result = await Runner.run(
            self.search_plan_agent,
            input_str
        )
        
        self.printer.mark_item_done("planning")
        return result.final_output_as(SearchPlan)

    async def _execute_searches(self, search_plan: SearchPlan) -> List[SearchResult]:
        """Execute searches in parallel"""
        self.printer.update_item("searching", "Searching for activities...")
        
        # Create a task for each search query
        tasks = []
        for query in search_plan.queries:
            input_str = (
                f"Search query: '{query.query}'\n"
                f"Reason: {query.reason}"
            )
            tasks.append(asyncio.create_task(Runner.run(self.search_agent, input_str)))
        
        # Wait for all searches to complete
        results = []
        num_completed = 0
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                results.append(result.final_output_as(SearchResult))
            except Exception:
                pass  # Skip failed searches
            
            num_completed += 1
            self.printer.update_item(
                "searching",
                f"Searching... {num_completed}/{len(tasks)} completed"
            )
            
        self.printer.mark_item_done("searching")
        return results

    async def _evaluate_activities(self, search_results: List[SearchResult], query: TripQuery) -> EvaluationResult:
        """Evaluate activities based on group composition"""
        self.printer.update_item("evaluating", "Evaluating activities for group...")
        
        # Format search results for the evaluation agent
        input_str = (
            f"Evaluate activities for a group of {query.participant_number} participants "
            f"with ages {query.participant_ages}.\n\n"
            f"Activities to evaluate: {[r.model_dump() for r in search_results]}"
        )
        
        result = await Runner.run(
            self.evaluation_agent,
            input_str
        )
        
        self.printer.mark_item_done("evaluating")
        return result.final_output_as(EvaluationResult)

    async def _generate_recommendations(
        self, 
        evaluated_activities: EvaluationResult, 
        weather_info: WeatherAnalysis, 
        query: TripQuery
    ) -> TripRecommendations:
        """Generate final trip recommendations"""
        self.printer.update_item("recommending", "Creating trip recommendations...")
        
        input_str = (
            f"Generate recommendations for a trip to {query.location} "
            f"from {query.start_date} to {query.end_date} "
            f"for {query.participant_number} participants (ages: {query.participant_ages}).\n\n"
            f"Weather information:\n{weather_info.model_dump()}\n\n"
            f"Evaluated activities:\n{evaluated_activities.model_dump()}"
        )
        
        result = await Runner.run(
            self.recommender_agent,
            input_str
        )
        
        self.printer.mark_item_done("recommending")
        return result.final_output_as(TripRecommendations)

    def _print_recommendations(self, recommendations: TripRecommendations) -> None:
        """Print the recommendations in a structured format"""
        print("\n=== Adventure Recommendations ===\n")
        print(f"\nWeather Summary:\n{recommendations.weather_summary}\n")
        
        print("\nRecommended Activities:")
        for activity in recommendations.recommended_activities:
            print(f"\n{activity.name}")
            print(f"Description: {activity.description}")
            print(f"Best Time: {activity.best_time}")
            if activity.source_url:
                print(f"More Info: {activity.source_url}")
            print("Weather Considerations:")
            for consideration in activity.weather_considerations:
                print(f"- {consideration}")
            print("Preparation Tips:")
            for tip in activity.preparation_tips:
                print(f"- {tip}")
            print(f"Group Notes: {activity.group_notes}")
        
        print("\nSuggested Daily Schedules:")
        for suggestion in recommendations.daily_schedule_suggestions:
            print(f"- {suggestion}")
        
        print("\nPacking List:")
        for item in recommendations.packing_list:
            print(f"- {item}")
        
        print("\nGeneral Tips:")
        for tip in recommendations.general_tips:
            print(f"- {tip}")
