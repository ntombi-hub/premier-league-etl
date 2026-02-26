# 🇿🇦 Premier League ETL — South African DStv Premiership

An end-to-end ETL pipeline for the **DStv Premiership** (South African Premier Soccer League). Extracts match results, standings, and team data from the API-Football API, transforms and validates it, then loads it into a PostgreSQL database for analysis.

---

## Architecture

```
API-Football
     │
     ▼
[extract.py] ──► data/raw/*.json   (raw backup)
     │
     ▼
[transform.py] ──► cleaned records
     │
     ▼
[validate]   ──► data quality checks
     │
     ▼
[load.py]    ──► PostgreSQL
     │
     ▼
[SQL Queries] ──► Analysis & Insights
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | ETL scripting |
| PostgreSQL | Data warehouse |
| Docker & Docker Compose | Local environment |
| GitHub Actions | Scheduled automation (daily) |
| API-Football | Data source |

---

## Questions This Pipeline Answers

- 📊 What are the current PSL standings?
- ⚽ Who won the Soweto Derby (Chiefs vs Pirates) historically?
- 🏠 Which team has the best home record this season?
- 🥅 Which teams have the most clean sheets?
- 📅 What months see the most goals in the PSL?
- 🌟 How dominant have Mamelodi Sundowns been over the last 3 seasons?

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- API-Football account (free tier at [api-sports.io](https://api-sports.io))

### 1. Clone the repo
```bash
git clone https://github.com/ntombi-hub/premier-league-etl.git
cd premier-league-etl
```

### 2. Set up your environment variables
```bash
cp .env.example .env
# Edit .env and add your API key and DB credentials
```

### 3. Start PostgreSQL with Docker
```bash
docker-compose up -d
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the pipeline
```bash
python src/pipeline.py
```

### 6. Query the data
Connect to the database using pgAdmin at `http://localhost:5050` or any SQL client, and run the queries in `sql/analysis_queries.sql`.

---

## Project Structure

```
premier-league-etl/
├── docker-compose.yml         # Postgres + pgAdmin
├── requirements.txt
├── .env.example               # Template for environment variables
├── .gitignore
├── .github/
│   └── workflows/
│       └── pipeline.yml       # Daily GitHub Actions schedule
├── src/
│   ├── extract.py             # Pulls data from API-Football
│   ├── transform.py           # Cleans and reshapes data
│   ├── load.py                # Inserts data into PostgreSQL
│   └── pipeline.py            # Runs the full ETL pipeline
├── sql/
│   ├── create_tables.sql      # Database schema
│   └── analysis_queries.sql   # Analytical SQL queries
└── data/
    └── raw/                   # Raw API responses (gitignored)
```

---

## Database Schema

```
dim_team ──────┐
               ├──► fact_matches
dim_team ──────┘

dim_team ──────► fact_standings

dim_player ────► dim_team
```

---

## Roadmap / V2 Ideas

- [ ] Add Apache Airflow for orchestration
- [ ] Add dbt for SQL transformations and testing
- [ ] Add a Streamlit dashboard for visualization
- [ ] Add player statistics tracking
- [ ] Add CAF Champions League data for Sundowns

---

## Data Source

Data provided by [API-Football](https://api-sports.io) — PSL League ID: `288`

---

## Author

Built by Ntombikayise Sibisi as a data engineering portfolio project.