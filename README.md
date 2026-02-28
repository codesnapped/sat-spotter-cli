# sat-spotter

CLI tool for predicting satellite passes over your location. Fetches real TLE data from Celestrak, computes pass times using SGP4 propagation, and displays results with elevation, direction, and duration.

Built with a focus on European/ESA satellites and the Polish space sector.

## Features

- Track multiple satellites (ISS, EagleEye, Sentinel-6A, and more)
- Pass prediction with rise/set times, max elevation, and compass directions
- **Visibility detection** — shows which passes are actually visible (sunlit satellite + dark sky)
- Color-coded elevation (green = great, yellow = ok, red = low)
- Local timezone support (defaults to Europe/Warsaw)
- TLE caching (4-hour expiry) to avoid repeated network requests
- Configurable via CLI flags and `satellites.json`

## Installation

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Default: 24h forecast for Warsaw
sat-spotter

# Custom location and time window
sat-spotter --lat 50.06 --lon 19.94 --hours 48

# Only show high-elevation passes
sat-spotter --elev 30

# Only show passes visible to the naked eye
sat-spotter --visible-only --hours 48

# Different timezone
sat-spotter --tz Europe/Berlin
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--lat` | 52.23 | Observer latitude |
| `--lon` | 21.01 | Observer longitude |
| `--hours` | 24 | Prediction window in hours |
| `--elev` | 10 | Minimum elevation in degrees |
| `--tz` | Europe/Warsaw | Timezone for display |
| `--visible-only` | false | Only show passes visible to the naked eye |

## Configuring satellites

Edit `satellites.json` to add or remove tracked satellites:

```json
[
    {"name": "ISS", "norad_id": 25544},
    {"name": "EagleEye", "norad_id": 60508},
    {"name": "Sentinel-6A", "norad_id": 46984}
]
```

Find NORAD IDs at [celestrak.org](https://celestrak.org/).

## Tech stack

- [skyfield](https://rhodesmill.org/skyfield/) — satellite position computation (SGP4)
- [httpx](https://www.python-httpx.org/) — HTTP client for TLE fetching
- [rich](https://rich.readthedocs.io/) — terminal table formatting
