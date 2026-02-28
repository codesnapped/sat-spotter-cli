from skyfield.api import wgs84
from skyfield.toposlib import GeographicPosition

def observer(latitude: float, longitude: float) -> GeographicPosition:
    return wgs84.latlon(latitude, longitude)