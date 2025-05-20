from langchain_core.tools import tool
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz
import datetime

@tool
def current_time() -> str:
    """
    Returns a formatted string of the current date including the hour, minutes, seconds, and miliseconds
    """
    return datetime.datetime.now()

@tool
def is_dark_outside(latitude: float, longitude: float, timezone: str) -> bool:
    """
    Returns true if it currently dark outside and false if otherwise
    """
    city = LocationInfo(latitude=latitude, longitude=longitude, timezone=timezone)
    s = sun(city.observer, date=datetime.datetime.now().date(), tzinfo=city.timezone)

    now = datetime.datetime.now(pytz.timezone(timezone))
    return now < s['sunrise'] or now > ['sunset']

@tool
def get_current_location() -> list:
    """
    Returns the latitude and longitude of Boston
    """
    return [{"latitude":42.3555}, {"longitude":-71.057083}]

@tool
def get_timezone() -> str:
    """
    Returns the timezone of Boston
    """
    return "America/New_York"