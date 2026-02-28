"""CLI entry point for Sat-Spotter."""


import json
from zoneinfo import ZoneInfo
from pathlib import Path
import argparse

from sat_spotter.display import group_passes, print_passes
from sat_spotter.location import observer
from sat_spotter.predict import find_passes
from sat_spotter.tle import fetch_tle, load_satellite, parse_tle


def main():

    parser = argparse.ArgumentParser(description="Satellite pass prediction")
    parser.add_argument("--lat", type=float, default=52.23, help="Observer location latitude")
    parser.add_argument("--lon", type=float, default=21.01, help="Observer location longitude")
    parser.add_argument("--hours", type=int, default=24, help="Hours to look ahead")
    parser.add_argument("--elev", type=int, default=10, help="Minimum elevation filter")
    parser.add_argument("--tz", type=str, default="Europe/Warsaw", help="Timezone for time display")
    parser.add_argument("--visible-only", dest="visible_only", action="store_true", help="Only show visible passes")
    args = parser.parse_args()

    observer_lat: float = args.lat
    observer_lon: float = args.lon
    chosen_timezone: ZoneInfo = ZoneInfo(args.tz)
    prediction_window: int = args.hours
    minimum_elevation_filter: int = args.elev
    show_only_visible: bool = args.visible_only

    config_path = Path(__file__).parent.parent.parent / "satellites.json"
    satellites = json.load(open(config_path))

    all_passes = []
    observer_location = observer(observer_lat, observer_lon)
    for s in satellites:
        satellite = load_satellite(parse_tle(fetch_tle(s["norad_id"])))
        if satellite is None:
            print(f"Skipping {s['name']}")
            continue
        times, _ = find_passes(satellite, observer_location, prediction_window)
        satellite_pass = group_passes(times, satellite, observer_location, minimum_elevation_filter)
        all_passes.extend(satellite_pass)

    all_passes.sort(key=lambda p: p['rise'].tt)
    print_passes(all_passes, chosen_timezone, observer_lat, observer_lon, show_only_visible)


if __name__ == "__main__":
    main()
