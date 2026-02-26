
-- ============================================
-- PSL Analysis Queries
-- DStv Premiership - South African Football
-- ============================================


-- 1. Current Season Standings
SELECT
    s.rank,
    t.name AS team,
    t.city,
    s.played,
    s.wins,
    s.draws,
    s.losses,
    s.goals_for,
    s.goals_against,
    s.goal_difference,
    s.points,
    s.form
FROM fact_standings s
JOIN dim_team t ON s.team_id = t.team_id
WHERE s.season = 2024
ORDER BY s.rank;


-- 2. Soweto Derby - Kaizer Chiefs vs Orlando Pirates Head to Head
SELECT
    m.match_date,
    ht.name AS home_team,
    m.home_goals,
    m.away_goals,
    at.name AS away_team,
    CASE
        WHEN m.home_goals > m.away_goals THEN ht.name
        WHEN m.away_goals > m.home_goals THEN at.name
        ELSE 'Draw'
    END AS result
FROM fact_matches m
JOIN dim_team ht ON m.home_team_id = ht.team_id
JOIN dim_team at ON m.away_team_id = at.team_id
WHERE (ht.name ILIKE '%Chiefs%' AND at.name ILIKE '%Pirates%')
   OR (ht.name ILIKE '%Pirates%' AND at.name ILIKE '%Chiefs%')
ORDER BY m.match_date DESC;


-- 3. Best Home Teams This Season
SELECT
    t.name AS team,
    t.city,
    COUNT(*) AS home_games,
    SUM(CASE WHEN m.home_goals > m.away_goals THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS home_draws,
    SUM(CASE WHEN m.home_goals < m.away_goals THEN 1 ELSE 0 END) AS home_losses,
    ROUND(SUM(CASE WHEN m.home_goals > m.away_goals THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS home_win_pct
FROM fact_matches m
JOIN dim_team t ON m.home_team_id = t.team_id
WHERE m.season = 2024 AND m.status = 'FT'
GROUP BY t.team_id, t.name, t.city
ORDER BY home_win_pct DESC;


-- 4. Best Away Teams This Season
SELECT
    t.name AS team,
    COUNT(*) AS away_games,
    SUM(CASE WHEN m.away_goals > m.home_goals THEN 1 ELSE 0 END) AS away_wins,
    ROUND(SUM(CASE WHEN m.away_goals > m.home_goals THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS away_win_pct
FROM fact_matches m
JOIN dim_team t ON m.away_team_id = t.team_id
WHERE m.season = 2024 AND m.status = 'FT'
GROUP BY t.team_id, t.name
ORDER BY away_win_pct DESC;


-- 5. Average Goals Per Game by Month
SELECT
    TO_CHAR(m.match_date, 'Month') AS month,
    EXTRACT(MONTH FROM m.match_date) AS month_num,
    COUNT(*) AS total_matches,
    SUM(m.home_goals + m.away_goals) AS total_goals,
    ROUND(AVG(m.home_goals + m.away_goals), 2) AS avg_goals_per_game
FROM fact_matches m
WHERE m.season = 2024 AND m.status = 'FT'
GROUP BY month, month_num
ORDER BY month_num;


-- 6. Most Clean Sheets This Season
SELECT
    t.name AS team,
    SUM(CASE WHEN m.home_team_id = t.team_id AND m.away_goals = 0 THEN 1
             WHEN m.away_team_id = t.team_id AND m.home_goals = 0 THEN 1
             ELSE 0 END) AS clean_sheets
FROM fact_matches m
JOIN dim_team t ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
WHERE m.season = 2024 AND m.status = 'FT'
GROUP BY t.team_id, t.name
ORDER BY clean_sheets DESC;


-- 7. Highest Scoring Matches
SELECT
    m.match_date,
    ht.name AS home_team,
    m.home_goals,
    m.away_goals,
    at.name AS away_team,
    (m.home_goals + m.away_goals) AS total_goals
FROM fact_matches m
JOIN dim_team ht ON m.home_team_id = ht.team_id
JOIN dim_team at ON m.away_team_id = at.team_id
WHERE m.season = 2024 AND m.status = 'FT'
ORDER BY total_goals DESC
LIMIT 10;


-- 8. Mamelodi Sundowns Dominance (Last 3 Seasons)
SELECT
    s.season,
    s.rank,
    s.points,
    s.wins,
    s.goal_difference
FROM fact_standings s
JOIN dim_team t ON s.team_id = t.team_id
WHERE t.name ILIKE '%Sundowns%'
ORDER BY s.season DESC;