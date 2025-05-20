from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
import os

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Fetches current weather for a given city"""
    
    api_key = ''
    if not api_key:
        return "Weather API key not found."
    
    url=f"http://api.openweathermap.org/data/2.5/weather?={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unknown error')}"
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        return f"The weather in {city} is {condition} with a temperature of {temp}"
    except Exception as e:
        return f"Failed to fetch weather: {e}"