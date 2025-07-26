import asyncio
from tools.weather_tools import get_weather_by_city, get_forecast_by_city

async def main():
    # Get current weather for Bengaluru
    print("Current Weather in Bengaluru:")
    weather = await get_weather_by_city("Bengaluru", "IN")
    print(weather)
    
    print("\n" + "="*50 + "\n")
    
    # Get 5-day forecast for Bengaluru
    print("5-Day Forecast for Bengaluru:")
    forecast = await get_forecast_by_city("Bengaluru", "IN")
    print(forecast)

if __name__ == "__main__":
    asyncio.run(main()) 