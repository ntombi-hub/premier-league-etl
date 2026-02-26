
------------
# Cleans and reshapes raw API data into structured records
# ready to be loaded into PostgreSQL.


from datetime import datetime
from loguru import logger


def transform_teams(raw_teams: list) -> list:
    """Transform raw team data into clean records."""
    logger.info("Transforming teams data...")
    teams = []

    for item in raw_teams:
        team = item.get("team", {})
        venue = item.get("venue", {})

        # Basic data quality check
        if not team.get("id") or not team.get("name"):
            logger.warning(f"Skipping team with missing id or name: {team}")
            continue

        teams.append({
            "team_id": team["id"],
            "name": team["name"],
            "short_name": team.get("code"),
            "country": team.get("country", "South Africa"),
            "founded": team.get("founded"),
            "stadium": venue.get("name"),
            "city": venue.get("city"),
            "logo_url": team.get("logo"),
        })

    logger.success(f"Transformed {len(teams)} teams")
    return teams


def transform_standings(raw_standings: list, season: int) -> list:
    """Transform raw standings data into clean records."""
    logger.info("Transforming standings data...")
    standings = []

    for item in raw_standings:
        team = item.get("team", {})

        if not team.get("id"):
            continue

        all_stats = item.get("all", {})
        goals = all_stats.get("goals", {})

        standings.append({
            "season": season,
            "team_id": team["id"],
            "rank": item.get("rank"),
            "points": item.get("points"),
            "played": all_stats.get("played"),
            "wins": all_stats.get("win"),
            "draws": all_stats.get("draw"),
            "losses": all_stats.get("lose"),
            "goals_for": goals.get("for"),
            "goals_against": goals.get("against"),
            "goal_difference": item.get("goalsDiff"),
            "form": item.get("form"),
        })

    logger.success(f"Transformed {len(standings)} standing records")
    return standings


def transform_matches(raw_matches: list, season: int) -> list:
    """Transform raw match data into clean records."""
    logger.info("Transforming matches data...")
    matches = []

    for item in raw_matches:
        fixture = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})

        match_id = fixture.get("id")
        if not match_id:
            continue

        # Parse date and time
        raw_date = fixture.get("date")
        match_date = None
        match_time = None
        if raw_date:
            dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            match_date = dt.date().isoformat()
            match_time = dt.time().isoformat()

        matches.append({
            "match_id": match_id,
            "season": season,
            "match_date": match_date,
            "match_time": match_time,
            "home_team_id": teams.get("home", {}).get("id"),
            "away_team_id": teams.get("away", {}).get("id"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),
            "status": fixture.get("status", {}).get("short"),
            "referee": fixture.get("referee"),
            "venue": fixture.get("venue", {}).get("name"),
        })

    logger.success(f"Transformed {len(matches)} match records")
    return matches


def validate_matches(matches: list) -> list:
    """Basic data quality checks on match records."""
    logger.info("Validating match data...")
    valid = []

    for m in matches:
        # Goals should not be negative
        if m["home_goals"] is not None and m["home_goals"] < 0:
            logger.warning(f"Skipping match {m['match_id']}: negative home goals")
            continue
        if m["away_goals"] is not None and m["away_goals"] < 0:
            logger.warning(f"Skipping match {m['match_id']}: negative away goals")
            continue
        # Must have both teams
        if not m["home_team_id"] or not m["away_team_id"]:
            logger.warning(f"Skipping match {m['match_id']}: missing team IDs")
            continue

        valid.append(m)

    logger.success(f"Validation complete: {len(valid)}/{len(matches)} matches passed")
    return valid



