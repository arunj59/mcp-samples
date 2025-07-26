from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional, Dict, Any
import re
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(r"C:\Users\Arun\IdeaProjects\mcp-samples\.env") # take environment variables

# Initialize FastMCP server
mcp = FastMCP("indian_railways")

# API Configuration
RAPID_API_KEY = config.get("ENV_RAPID_API_KEY")
RAPID_API_HOST = "indian-railway-irctc.p.rapidapi.com"

def validate_train_number(train_number: str) -> bool:
    """Validate train number format (4-5 digits)."""
    return bool(re.match(r'^\d{4,5}$', train_number))

@mcp.tool()
async def get_train_info(train_number: str) -> str:
    """Get basic information about a train.
    
    Args:
        train_number: The train number to look up (4-5 digits)
        
    Returns:
        Formatted string containing train information
    """
    if not validate_train_number(train_number):
        return "Invalid train number. Please provide a 4-5 digit number."

    url = f"https://indian-railway-irctc.p.rapidapi.com/api/trains-search/v1/train/{train_number}"
    
    querystring = {
        "isH5": "true",
        "client": "web"
    }
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST,
        "x-rapid-api": "rapid-api-database"
    }
    
    try:
        print(f"\nGetting information for train {train_number}...")
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "body" in data and data["body"]:
                trains = data["body"][0].get("trains", [])
                if trains:
                    train = trains[0]
                    result = f"""
Train Details:
Number: {train.get('trainNumber', 'N/A')}
Name: {train.get('trainName', 'N/A')}
From: {train.get('origin', 'N/A')}
To: {train.get('destination', 'N/A')}
Type: {', '.join(train.get('train_type', ['N/A']))}
Classes: {', '.join(train.get('journeyClasses', ['N/A']))}

Schedule:"""
                    
                    schedule = train.get("schedule", [])
                    if schedule:
                        for stop in schedule:
                            result += f"""
• {stop.get('stationName', 'N/A')} ({stop.get('stationCode', 'N/A')})
  Arrival: {stop.get('arrivalTime', '--')} | Departure: {stop.get('departureTime', '--')}
  Distance: {stop.get('distance', 'N/A')} km"""
                    return result
                return "Train details not found."
            return "No data found for this train."
        else:
            return f"Error response: {response.text}"
    except Exception as e:
        return f"Error occurred: {e}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
