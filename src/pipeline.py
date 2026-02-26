import os 
from dotenv import load_dotenv
from loguru import logger 

from extract import get_teams, get_standings , get_matches
from  transform import transform_teams , transform_standing, transform_matches, validate_matches
from load import load_teams, load_standings, load_matches 

load_dotenv()

CURRENT_SEASON = int(os.getenv("CURRENT_SEASON", 2026))


def run_pipeline():
    logger.info("=" * 50)
    logger.info("PSL DATA PIPELINE STARTING")
    logger.info(f"Season: {CURRENT_SEASON}")
    logger.info("=" * 50)

    try:
#EXTRACT
        logger.info("STEP 1: Extracting data from API...")
        raw_teams = get_teams()
        raw_standings = get_standings()
        raw_matches = get_matches(CURRENT_SEASON)

        #TRANSFORM
        logger.info("STEP 2: Transfroming data...")
        teams = transform_teams(raw_teams)
        standings = transform_standings(raw_standings, CURRENT_SEASON)
        matches = transform_matches(raw_matches, CURRENT_SEASON)

        #Validate
        logger.info("STEP 3: Validating data...")
        matches = validate_matches(matches)

        #LOAD
        logger.info("STEP 4: Loading data into PostgreSQL...")
        load_teams(teams)
        load_standings(standings)
        load_matches(matches)

        logger.info("=" * 50)
        logger.success("PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info(f"  Teams loaded: {len(teams)}")
        logger.info(f"  Standings loaded:{len(standings)}")
        logger.info(f"  Matches loaded: {len(matches)}")


    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise 


if __name__ == "__main__":
    run_pipeline()





    

