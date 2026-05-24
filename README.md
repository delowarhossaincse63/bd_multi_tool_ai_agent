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

## What to keep out of GitHub

Do not push these files to GitHub:

- `.env` (contains API keys)
- `dbs/*.db` (database files)
- `venv/` or `.venv/` (local virtual environment)
- `__pycache__/` and `.pyc` files

Your `.gitignore` already excludes these files.

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

## Recommended commit message

```text
git commit -m "Initial project submission: BD Agent with data ingestion and agent tools"
```
