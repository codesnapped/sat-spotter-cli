from pathlib import Path


CONFIG_PATH = Path(__file__).parent.parent.parent / "satellites.json"
BASE_CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache"
DEFAULT_CACHE_DURATION = 4 * 3600
