from enum import Enum
import json
from typing import Sequence, Any, Dict

import httpx
from pydantic import BaseModel
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError


class WeatherTools(str, Enum):
    GET_CURRENT_WEATHER = "get_current_weather"
    GET_FORECAST = "get_forecast"


class CurrentWeatherResult(BaseModel):
    location: Dict[str, float]
    temperature: float
    apparent_temperature: float
    is_day: bool
    precipitation: float
    humidity: float
    wind_speed: float
    wind_direction: int
    cloud_cover: int
    pressure: float
    weather_code: int


class ForecastResult(BaseModel):
    location: Dict[str, float]
    daily_forecasts: list[Dict[str, Any]]


# Constants
OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
USER_AGENT = "mcp-server-weather/0.1.0"


async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise McpError(f"Error fetching weather data: {str(e)}")


class WeatherServer:
    async def get_current_weather(self, latitude: float, longitude: float) -> CurrentWeatherResult:
        """Get current weather for a location."""
        url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,precipitation,relative_humidity_2m,apparent_temperature,weather_code"
        data = await make_openmeteo_request(url)
        
        if not data or "current" not in data:
            raise McpError("Unable to fetch current weather data for this location.")
        
        current = data["current"]
        
        return CurrentWeatherResult(
            location={"latitude": latitude, "longitude": longitude},
            temperature=current.get("temperature_2m", 0.0),
            apparent_temperature=current.get("apparent_temperature", 0.0),
            is_day=bool(current.get("is_day", 0)),
            precipitation=current.get("precipitation", 0.0),
            humidity=current.get("relative_humidity_2m", 0.0),
            wind_speed=current.get("wind_speed_10m", 0.0),
            wind_direction=current.get("wind_direction_10m", 0),
            cloud_cover=current.get("cloud_cover", 0),
            pressure=current.get("pressure_msl", 0.0),
            weather_code=current.get("weather_code", 0)
        )

    async def get_forecast(self, latitude: float, longitude: float) -> ForecastResult:
        """Get weather forecast for a location."""
        url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto"
        data = await make_openmeteo_request(url)
        
        if not data or "daily" not in data:
            raise McpError("Unable to fetch forecast data for this location.")
        
        daily = data["daily"]
        forecasts = []
        
        for i in range(len(daily["time"])):
            forecast = {
                "date": daily["time"][i],
                "max_temperature": daily["temperature_2m_max"][i],
                "min_temperature": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "weather_code": daily["weathercode"][i]
            }
            forecasts.append(forecast)
        
        return ForecastResult(
            location={"latitude": latitude, "longitude": longitude},
            daily_forecasts=forecasts
        )


async def serve() -> None:
    server = Server("mcp-weather")
    weather_server = WeatherServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available weather tools."""
        return [
            Tool(
                name=WeatherTools.GET_CURRENT_WEATHER.value,
                description="Get current weather conditions for a location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Latitude of the location",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Longitude of the location",
                        },
                    },
                    "required": ["latitude", "longitude"],
                },
            ),
            Tool(
                name=WeatherTools.GET_FORECAST.value,
                description="Get weather forecast for a location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Latitude of the location",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Longitude of the location",
                        },
                    },
                    "required": ["latitude", "longitude"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for weather queries."""
        try:
            match name:
                case WeatherTools.GET_CURRENT_WEATHER.value:
                    latitude = arguments.get("latitude")
                    longitude = arguments.get("longitude")
                    
                    if latitude is None or longitude is None:
                        raise ValueError("Missing required arguments: latitude and longitude")

                    result = await weather_server.get_current_weather(latitude, longitude)

                case WeatherTools.GET_FORECAST.value:
                    latitude = arguments.get("latitude")
                    longitude = arguments.get("longitude")
                    
                    if latitude is None or longitude is None:
                        raise ValueError("Missing required arguments: latitude and longitude")

                    result = await weather_server.get_forecast(latitude, longitude)
                
                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [
                TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
            ]

        except Exception as e:
            raise ValueError(f"Error processing mcp-server-weather query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options) 