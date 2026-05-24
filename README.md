# BD Agent

A simple AI agent for Bangladeshi datasets. This project loads three HuggingFace datasets into SQLite databases, exposes SQL tools for hospitals, institutions, and restaurants, and adds a web search tool for general knowledge.

## Project structure

- `agent.py` — main program that builds the LangChain agent and runs queries
- `ingest.py` — downloads datasets and creates SQLite files in `dbs/`
- `tools/db_tools.py` — builds SQL tools for each database
- `tools/web_search_tool.py` — builds a SerpAPI search tool
- `requirements.txt` — Python dependencies
- `.env.example` — environment variable template
- `.gitignore` — files and folders to exclude from Git
 
## High-level architecture

- `ingest.py` downloads datasets from HuggingFace, normalizes column names, and writes each dataset as a single table in a SQLite file under `dbs/`.
- `tools/db_tools.py` exposes simple LangChain SQL tools that run SQL queries against those SQLite databases.
- `tools/web_search_tool.py` wraps SerpAPI for general web queries.
- `agent.py` composes the LLM and registered tools into a single agent that chooses the correct tool for incoming questions.

## What to keep out of GitHub

Do not push these files to GitHub:

- `.env` (contains API keys)
- `dbs/*.db` (database files)
- `venv/` or `.venv/` (local virtual environment)
- `__pycache__/` and `.pyc` files

Your `.gitignore` already excludes these files.

If you accidentally commit a secret (API key) to the repo, do NOT push it. Remove it from the file and use `git commit --amend` or an interactive rebase to purge it from history, then force-push. See the Troubleshooting section below for commands.

## Setup

1. Open terminal in the project folder:

```powershell
cd "c:\Users\hp\Documents\bd agent"
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create `.env` from the example:

```powershell
copy .env.example .env
```

5. Open `.env` and add your keys:

```text
OPENAI_API_KEY=your_openai_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

## Build the databases

Run the ingestion script to download datasets and create the SQLite databases:

```powershell
python ingest.py
```

After this, the project will create:

- `dbs/institutions.db`
- `dbs/hospitals.db`
- `dbs/restaurants.db`

### How ingestion works (details)

- `ingest.py` calls `datasets.load_dataset(dataset_name, split="train")` for each dataset listed in the script.
- The dataset is converted to a `pandas.DataFrame`, column names are normalized (lowercase, non-alphanumeric -> underscore), and duplicate column names are de-duplicated by suffixing `_2`, `_3`, etc.
- Each dataframe is saved to a SQLite database using `df.to_sql(table_name, conn, if_exists="replace", index=False)`.

### Datasets used (sources)

- `Mahadih534/Institutional-Information-of-Bangladesh` → `institutions` table
- `Mahadih534/all-bangladeshi-hospitals` → `hospitals` table
- `Mahadih534/Bangladeshi-Restaurant-Data` → `restaurants` table

To add another dataset, add a `save_dataset_to_db(dataset_name, table_name, db_path)` call in `ingest.py`.

## Run the agent

Run the agent and type your question when prompted:

```powershell
python agent.py
```

Or run a direct query:

```powershell
python agent.py "How many hospitals are in Dhaka?"
```

## Example queries

- `How many hospitals are in Dhaka?`
- `List hospitals with ICU facilities in Chittagong.`
- `What universities are listed in the institutions database?`
- `Show popular restaurants serving Bengali cuisine in Sylhet.`
- `What is the role of DGHS in Bangladesh?`

## Notes for submission

- Keep `.env` out of the repository.
- If you want the repository to be ready for review, include `.env.example` instead of `.env`.
- If your teacher wants the project to run without downloading datasets, you can remove `dbs/*.db` from `.gitignore`, commit the DB files, and mention that the databases are already built.

## Submission checklist

Before sharing the GitHub link with your instructor, make sure:

- `.env` is not tracked (should be listed in `.gitignore`).
- `README.md`, `requirements.txt`, and `ingest.py` are present and up-to-date.
- `.env.example` contains placeholders (no real secrets).
- Optionally include `dbs/*.db` only if your instructor asked for prebuilt databases.

Include the repository link and a short run command for the reviewer:

```powershell
git clone https://github.com/delowarhossaincse63/bd_multi_tool_ai_agent.git
cd bd_multi_tool_ai_agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# add your API keys into .env, then run:
python ingest.py
python agent.py "How many hospitals are in Dhaka?"
```

## Submission Requirements

This repository meets the submission requirements:

- GitHub repo with full codebase (`agent.py`, `ingest.py`, `tools/`, `requirements.txt`, `.env.example`, `.gitignore`, `README.md`).
- `README.md` with setup and usage instructions.
- Optional demo: create a Google Colab link if needed by the reviewer.

## Recommended commit message

```text
git commit -m "Initial project submission: BD Agent with data ingestion and agent tools"
```

## Database inspection & quick checks

You can inspect the generated SQLite databases in a few ways.

- Using the `sqlite3` CLI (if installed):

```bash
sqlite3 dbs/hospitals.db "PRAGMA table_info('hospitals');"
sqlite3 dbs/hospitals.db "SELECT COUNT(*) FROM hospitals;"
```

- Using Python (works on Windows):

```python
import sqlite3
conn = sqlite3.connect('dbs/hospitals.db')
cur = conn.cursor()
print(cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
print(cur.execute("SELECT count(*) FROM hospitals;").fetchone())
conn.close()
```

If a table name differs, replace `hospitals` with the printed table name.

## Tools and code overview

- `tools/db_tools.py` — contains helper functions `get_hospitals_tool()`, `get_institutions_tool()`, `get_restaurants_tool()` that return LangChain-compatible tools. Each tool runs SQL queries against the corresponding database and returns results formatted for the agent.
- `tools/web_search_tool.py` — builds a simple web-search wrapper using SerpAPI. If `SERPAPI_API_KEY` is missing, the web tool will not work and the agent should fall back to SQL tools.

## Troubleshooting

- "OPENAI_API_KEY is required" error: ensure `.env` exists and contains `OPENAI_API_KEY`. Then restart the process/terminal so `load_dotenv()` picks it up.
- Secret scanning block on push: if GitHub rejects a push because it found a secret in a commit, remove the secret from the file, amend the commit (or remove it from history), and push again. Example commands:

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git commit --amend --no-edit  # to fix last commit if needed
git push -f origin main
```

- If agent output seems incorrect or tools are not invoked, check the console for tracebacks and ensure required keys are present in `.env`.

## Testing quickly

1. Build DBs:

```powershell
python ingest.py
```

2. Run a sample query:

```powershell
python agent.py "How many hospitals are in Dhaka?"
```
## Contact

If you need to reach me about this submission, contact: Delowar Hossain <delowarhm19@gmail.com>
