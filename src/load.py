

# Loads cleaned and transformed data into PostgreSQL.
# Uses upserts (INSERT ... ON CONFLICT) so the pipeline
# can be safely re-run without creating duplicates.



import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def get_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def load_teams(teams: list):
    """Load team records into dim_team table."""
    if not teams:
        logger.warning("No teams to load.")
        return

    logger.info(f"Loading {len(teams)} teams into dim_team...")
    sql = """
        INSERT INTO dim_team (team_id, name, short_name, country, founded, stadium, city, logo_url)
        VALUES %s
        ON CONFLICT (team_id) DO UPDATE SET
            name       = EXCLUDED.name,
            short_name = EXCLUDED.short_name,
            stadium    = EXCLUDED.stadium,
            city       = EXCLUDED.city,
            logo_url   = EXCLUDED.logo_url;
    """
    records = [
        (
            t["team_id"], t["name"], t["short_name"], t["country"],
            t["founded"], t["stadium"], t["city"], t["logo_url"]
        )
        for t in teams
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, records)
        conn.commit()

    logger.success(f"Loaded {len(teams)} teams")


def load_standings(standings: list):
    """Load standings records into fact_standings table."""
    if not standings:
        logger.warning("No standings to load.")
        return

    logger.info(f"Loading {len(standings)} standings into fact_standings...")
    sql = """
        INSERT INTO fact_standings (season, team_id, rank, points, played, wins, draws, losses, goals_for, goals_against, goal_difference, form)
        VALUES %s
        ON CONFLICT (season, team_id) DO UPDATE SET
            rank            = EXCLUDED.rank,
            points          = EXCLUDED.points,
            played          = EXCLUDED.played,
            wins            = EXCLUDED.wins,
            draws           = EXCLUDED.draws,
            losses          = EXCLUDED.losses,
            goals_for       = EXCLUDED.goals_for,
            goals_against   = EXCLUDED.goals_against,
            goal_difference = EXCLUDED.goal_difference,
            form            = EXCLUDED.form,
            updated_at      = CURRENT_TIMESTAMP;
    """
    records = [
        (
            s["season"], s["team_id"], s["rank"], s["points"], s["played"],
            s["wins"], s["draws"], s["losses"], s["goals_for"],
            s["goals_against"], s["goal_difference"], s["form"]
        )
        for s in standings
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, records)
        conn.commit()

    logger.success(f"Loaded {len(standings)} standing records")


def load_matches(matches: list):
    """Load match records into fact_matches table."""
    if not matches:
        logger.warning("No matches to load.")
        return

    logger.info(f"Loading {len(matches)} matches into fact_matches...")
    sql = """
        INSERT INTO fact_matches (match_id, season, match_date, match_time, home_team_id, away_team_id, home_goals, away_goals, status, referee, venue)
        VALUES %s
        ON CONFLICT (match_id) DO UPDATE SET
            home_goals = EXCLUDED.home_goals,
            away_goals = EXCLUDED.away_goals,
            status     = EXCLUDED.status,
            referee    = EXCLUDED.referee;
    """
    records = [
        (
            m["match_id"], m["season"], m["match_date"], m["match_time"],
            m["home_team_id"], m["away_team_id"], m["home_goals"],
            m["away_goals"], m["status"], m["referee"], m["venue"]
        )
        for m in matches
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, records)
        conn.commit()

    logger.success(f"Loaded {len(matches)} match records") 
    


            
    



