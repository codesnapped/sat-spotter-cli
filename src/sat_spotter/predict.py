from skyfield.api import load
from skyfield.api import EarthSatellite
from skyfield.toposlib import GeographicPosition

def find_passes(satellite: EarthSatellite, location: GeographicPosition, hours) -> tuple:
    ts = load.timescale()
    t0 = ts.now()
    t1 = ts.tt_jd(t0.tt + hours / 24.0)
    return satellite.find_events(location, t0, t1)