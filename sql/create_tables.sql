
-- ============================================
-- PSL Data Pipeline - Database Schema
-- DStv Premiership (South African Football)
-- ============================================

-- Drop tables if they exist (for clean resets)
DROP TABLE IF EXISTS fact_standings CASCADE;
DROP TABLE IF EXISTS fact_matches CASCADE;
DROP TABLE IF EXISTS dim_player CASCADE;
DROP TABLE IF EXISTS dim_team CASCADE;

-- ============================================
-- DIMENSION TABLES
-- ============================================

CREATE TABLE dim_team (
    team_id     INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    short_name  VARCHAR(20),
    country     VARCHAR(50) DEFAULT 'South Africa',
    founded     INT,
    stadium     VARCHAR(100),
    city        VARCHAR(50),
    logo_url    VARCHAR(255),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_player (
    player_id   INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    firstname   VARCHAR(50),
    lastname    VARCHAR(50),
    nationality VARCHAR(50),
    position    VARCHAR(30),
    age         INT,
    team_id     INT REFERENCES dim_team(team_id),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- FACT TABLES
-- ============================================

CREATE TABLE fact_matches (
    match_id        INT PRIMARY KEY,
    season          INT NOT NULL,
    match_date      DATE,
    match_time      TIME,
    home_team_id    INT REFERENCES dim_team(team_id),
    away_team_id    INT REFERENCES dim_team(team_id),
    home_goals      INT,
    away_goals      INT,
    status          VARCHAR(20),  -- 'FT', 'NS', 'LIVE'
    referee         VARCHAR(100),
    venue           VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_standings (
    id              SERIAL PRIMARY KEY,
    season          INT NOT NULL,
    team_id         INT REFERENCES dim_team(team_id),
    rank            INT,
    points          INT,
    played          INT,
    wins            INT,
    draws           INT,
    losses          INT,
    goals_for       INT,
    goals_against   INT,
    goal_difference INT,
    form            VARCHAR(10),  -- e.g. 'WWDLL'
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (season, team_id)
);

-- ============================================
-- INDEXES for query performance
-- ============================================

CREATE INDEX idx_matches_season ON fact_matches(season);
CREATE INDEX idx_matches_date ON fact_matches(match_date);
CREATE INDEX idx_matches_home_team ON fact_matches(home_team_id);
CREATE INDEX idx_matches_away_team ON fact_matches(away_team_id);
CREATE INDEX idx_standings_season ON fact_standings(season);
CREATE INDEX idx_player_team ON dim_player(team_id);
