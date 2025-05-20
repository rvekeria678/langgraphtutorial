from langchain_core.tools import tool
import requests

@tool
def get_astronaut_names() -> list:
    """
    Returns a list of names of the astronauts currently in space.
    """
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    data = response.json()
    return data['people']

@tool
def get_iss_location() -> list:
    """
    Returns the current latitude and longitude of the ISS as a formatted string.
    """
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()

    return data['iss_position']