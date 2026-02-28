import httpx
from skyfield.api import EarthSatellite, load
from pathlib import Path
import time

BASE_CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache"

def read_cache(norad_id: int) -> str | None:
    DEFAULT_CACHE_DURATION = 4 * 3600

    cache_file = BASE_CACHE_DIR / f"{norad_id}.tle"
    cache_data: str | None = None

    if cache_file.exists():
        data_age = time.time() - cache_file.stat().st_mtime
        if data_age < DEFAULT_CACHE_DURATION:
            cache_data = cache_file.read_text()
    
    return cache_data

def write_cache(norad_id: int, data: str):
    BASE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = BASE_CACHE_DIR / f"{norad_id}.tle"
    cache_file.write_text(data)

def fetch_tle(norad_id: int) -> str | None:
    cache_data = read_cache(norad_id)
    if cache_data is not None:
        return cache_data

    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        write_cache(norad_id, response.text)
        return response.text
    except httpx.HTTPError as e:
        print(f"Failed to fetch TLE for {norad_id}: {e}")
        return None

def parse_tle(tle_data: str) -> dict:
    if tle_data is None:
        return None
    data = tle_data.strip().splitlines()
    if len(data) < 3 or not data[1].startswith("1 ") or not data[2].startswith("2 "):
        return None
    return {
        "name": data[0].strip(),
        "line1": data[1].strip(),
        "line2": data[2].strip(),
    }

def load_satellite(tle_data: dict) -> EarthSatellite:
    if tle_data is None:
        return None
    ts = load.timescale()
    return EarthSatellite(tle_data["line1"], tle_data["line2"], tle_data["name"], ts)