from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import dotenv_values

config = dotenv_values(r"C:\Users\Arun\IdeaProjects\mcp-samples\.env") # take environment variables

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5"
USER_AGENT = "weather-app/1.0"
OPENWEATHER_API_KEY = config.get("ENV_OPENWEATHER_API_KEY")

async def make_weather_request(url: str, params: dict) -> dict[str, Any] | None:
    """Make a request to the OpenWeatherMap API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making weather request: {str(e)}")
            return None

def format_weather(data: dict) -> str:
    """Format weather data into a readable string."""
    if not data:
        return "Unable to fetch weather data."
    
    try:
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        
        # Get probability of precipitation if available
        pop = data.get("pop", None)
        pop_text = f"\nChance of Rain: {int(pop * 100)}%" if pop is not None else ""
        
        return f"""
Current Weather:
Temperature: {main.get('temp', 'N/A')}°C
Feels Like: {main.get('feels_like', 'N/A')}°C
Condition: {weather.get('main', 'N/A')} - {weather.get('description', 'N/A')}
Humidity: {main.get('humidity', 'N/A')}%
Wind Speed: {wind.get('speed', 'N/A')} m/s
Pressure: {main.get('pressure', 'N/A')} hPa{pop_text}
"""
    except (KeyError, IndexError):
        return "Error formatting weather data."

def format_forecast(data: dict) -> str:
    """Format forecast data into a readable string."""
    if not data or "list" not in data:
        return "Unable to fetch forecast data."
    
    try:
        forecasts = []
        for item in data["list"][:5]:  # Get next 5 forecasts
            dt_txt = item.get("dt_txt", "N/A")
            main = item["main"]
            weather = item["weather"][0]
            
            # Get probability of precipitation (0-1 scale, convert to percentage)
            pop = item.get("pop", 0)
            pop_percentage = int(pop * 100)
            
            forecast = f"""
Time: {dt_txt}
Temperature: {main.get('temp', 'N/A')}°C
Condition: {weather.get('main', 'N/A')} - {weather.get('description', 'N/A')}
Humidity: {main.get('humidity', 'N/A')}%
Chance of Rain: {pop_percentage}%
"""
            forecasts.append(forecast)
        
        return "\n---\n".join(forecasts)
    except (KeyError, IndexError):
        return "Error formatting forecast data."

@mcp.tool()
async def get_weather_by_city(city: str, country_code: str = "") -> str:
    """Get current weather for a city.
    
    Args:
        city: Name of the city
        country_code: Two-letter country code (optional)
    """
    location = f"{city},{country_code}" if country_code else city
    
    # Get current weather
    weather_url = f"{OPENWEATHER_API_BASE}/weather"
    weather_params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    weather_data = await make_weather_request(weather_url, weather_params)
    
    if not weather_data:
        return "Unable to fetch weather data for this location."
    
    # Get short-term forecast for precipitation probability
    forecast_url = f"{OPENWEATHER_API_BASE}/forecast"
    forecast_params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "cnt": 1  # Get only the first forecast period
    }
    
    forecast_data = await make_weather_request(forecast_url, forecast_params)
    
    # Add precipitation probability to weather data if available
    if forecast_data and "list" in forecast_data and len(forecast_data["list"]) > 0:
        weather_data["pop"] = forecast_data["list"][0].get("pop", 0)
    
    return format_weather(weather_data)

@mcp.tool()
async def get_forecast_by_city(city: str, country_code: str = "") -> str:
    """Get 5-day weather forecast for a city.
    
    Args:
        city: Name of the city
        country_code: Two-letter country code (optional)
    """
    location = f"{city},{country_code}" if country_code else city
    url = f"{OPENWEATHER_API_BASE}/forecast"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    data = await make_weather_request(url, params)
    
    if not data:
        return "Unable to fetch forecast data for this location."
    
    return format_forecast(data)

@mcp.tool()
async def get_weather_by_coords(latitude: float, longitude: float) -> str:
    """Get current weather for coordinates.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = f"{OPENWEATHER_API_BASE}/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    data = await make_weather_request(url, params)
    
    if not data:
        return "Unable to fetch weather data for this location."
    
    return format_weather(data)

@mcp.tool()
async def get_forecast_by_coords(latitude: float, longitude: float) -> str:
    """Get 5-day weather forecast for coordinates.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = f"{OPENWEATHER_API_BASE}/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    data = await make_weather_request(url, params)
    
    if not data:
        return "Unable to fetch forecast data for this location."
    
    return format_forecast(data)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')