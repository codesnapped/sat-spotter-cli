from skyfield.api import EarthSatellite
from skyfield.toposlib import GeographicPosition


def plot_pass(pass_data, satellite: EarthSatellite, location: GeographicPosition):
    return