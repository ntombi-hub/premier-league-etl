# Pulls data from API-Football for the PSL
# Saves raw responses as JSON files for traceability

import os
import json
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://v3.football.api-sports.io")
PSL_LEAGUE_ID = int(os.getenv("PSL_LEAGUE_ID", 288))
CURRENT_SEASON = int(os.getenv("CURRENT_SEASON", 2024))

HEADERS = {"x-apisports-key": API_KEY}

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


def save_raw(data: dict, filename: str):
    """Save raw API response to JSON file for traceability."""
    filepath = os.path.join(RAW_DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Raw data saved to {filepath}")


def get_teams() -> list:
    """Fetch all PSL teams."""
    logger.info("Extracting PSL teams...")
    url = f"{API_BASE_URL}/teams"
    params = {"league": PSL_LEAGUE_ID, "season": CURRENT_SEASON}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("response"):
        logger.warning("No teams returned from API")
        return []

    save_raw(data, f"teams_{CURRENT_SEASON}.json")
    teams = data["response"]
    logger.success(f"Extracted {len(teams)} teams")
    return teams


def get_standings() -> list:
    """Fetch PSL league standings."""
    logger.info("Extracting PSL standings...")
    url = f"{API_BASE_URL}/standings"
    params = {"league": PSL_LEAGUE_ID, "season": CURRENT_SEASON}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("response"):
        logger.warning("No standings returned from API")
        return []

    save_raw(data, f"standings_{CURRENT_SEASON}.json")
    standings = data["response"][0]["league"]["standings"][0]
    logger.success(f"Extracted standings for {len(standings)} teams")
    return standings


def get_matches(season: int = None) -> list:
    """Fetch PSL matches for a given season."""
    if season is None:
        season = CURRENT_SEASON
    logger.info(f"Extracting PSL matches for season {season}...")
    url = f"{API_BASE_URL}/fixtures"
    params = {"league": PSL_LEAGUE_ID, "season": season}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("response"):
        logger.warning("No matches returned from API")
        return []

    save_raw(data, f"matches_{season}.json")
    matches = data["response"]
    logger.success(f"Extracted {len(matches)} matches")
    return matches


if __name__ == "__main__":
    logger.info("Starting extraction")
    teams = get_teams()
    standings = get_standings()
    matches = get_matches()
    logger.success("Extraction complete!")
