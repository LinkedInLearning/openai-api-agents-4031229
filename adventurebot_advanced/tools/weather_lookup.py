# A basic weather lookup tool using Open-Meteo API

import json
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import httpx
from pydantic import BaseModel

from agents import function_tool


class WeatherForecast(BaseModel):
    """Weather forecast data from Open-Meteo API"""
    latitude: float
    longitude: float
    temperature_2m: list[float]
    relative_humidity_2m: list[float]
    apparent_temperature: list[float]
    precipitation_probability: list[float]
    precipitation: list[float]
    rain: list[float]
    showers: list[float]
    snowfall: list[float]
    snow_depth: list[float]
    visibility: list[float]
    wind_speed_10m: list[float]
    wind_direction_10m: list[float]
    wind_gusts_10m: list[float]
    cloud_cover: list[float]
    uv_index: list[float]
    timestamps: list[str]


@function_tool
async def get_weather_forecast(location: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> WeatherForecast:
    """Get weather forecast for a location and date range using Open-Meteo API.
    
    Args:
        location: City name or coordinates (lat,lon)
        start_date: Start date in YYYY-MM-DD format. Defaults to today.
        end_date: End date in YYYY-MM-DD format. Defaults to 7 days from start.
    
    Returns:
        WeatherForecast object containing hourly weather data
    """
    # Parse location into lat/lon
    # For simplicity using fixed coordinates, but you could use a geocoding service here
    lat, lon = 52.52, 13.41  # Default to Berlin
    if ',' in location:
        try:
            lat, lon = map(float, location.split(','))
        except ValueError:
            pass
            
    # Handle dates
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    if not end_date:
        end_date = (datetime.strptime(start_date, '%Y-%m-%d')).strftime('%Y-%m-%d')

    # Construct API URL
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,"
        f"visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover,uv_index"
        f"&start_date={quote(start_date)}&end_date={quote(end_date)}"
    )

    # Make API request
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    # Parse response into WeatherForecast model
    hourly = data['hourly']
    return WeatherForecast(
        latitude=data['latitude'],
        longitude=data['longitude'],
        temperature_2m=hourly['temperature_2m'],
        relative_humidity_2m=hourly['relative_humidity_2m'],
        apparent_temperature=hourly['apparent_temperature'],
        precipitation_probability=hourly['precipitation_probability'],
        precipitation=hourly['precipitation'],
        rain=hourly['rain'],
        showers=hourly['showers'],
        snowfall=hourly['snowfall'],
        snow_depth=hourly['snow_depth'],
        visibility=hourly['visibility'],
        wind_speed_10m=hourly['wind_speed_10m'],
        wind_direction_10m=hourly['wind_direction_10m'],
        wind_gusts_10m=hourly['wind_gusts_10m'],
        cloud_cover=hourly['cloud_cover'],
        uv_index=hourly['uv_index'],
        timestamps=hourly['time']
    )
