# 🇧🇩 BD Agent — Multi-Tool AI Agent for Bangladesh

An AI assistant that can answer real questions about Bangladesh — hospitals, educational institutions, and restaurants — by searching real datasets, and falls back to the web for anything else.

Ask it things like:

> "How many hospitals are in Dhaka?"
> "List hospitals with ICU facilities in Chittagong."
> "Show popular restaurants serving Bengali cuisine in Sylhet."
> "What is the role of DGHS in Bangladesh?"

...and it will figure out *which data source to use* and give you a real answer.

---

## 🤔 What is this project?

This is a **Python-based AI agent** — a program that combines a large language model (like GPT) with a set of "tools" it can choose from to answer questions, instead of just guessing from memory.

Concretely, it:

1. Downloads three real datasets about Bangladesh from HuggingFace (hospitals, institutions, restaurants).
2. Stores them as local SQLite databases.
3. Gives an AI agent (built with **LangChain**) the ability to query those databases directly using SQL — so answers come from real data, not hallucinated guesses.
4. Adds a **web search tool** (via SerpAPI) for general questions that aren't in the datasets.
5. Lets the agent decide, per question, which tool is the right one to use.

## 💡 Why this project exists

Most general-purpose AI chatbots don't have accurate, structured, up-to-date information specific to Bangladesh — things like which hospitals have ICUs, which universities exist, or what restaurants are popular in a given city. This project solves that by:

- Grounding answers in **real, structured datasets** instead of relying on an LLM's memory (which reduces hallucination).
- Demonstrating a practical, working example of a **tool-using AI agent** — a pattern that's increasingly important in real-world AI applications.
- Being a reusable template: anyone can plug in a new Bangladesh (or any country) dataset and instantly get a new queryable tool.

In short: **it's a small, working example of how to build a trustworthy, data-grounded AI agent** — useful both as a learning project and as a real, functional assistant.

---

## 🗂️ Project Structure

```
bd_multi_tool_ai_agent/
├── agent.py                  # Main entry point — builds & runs the AI agent
├── ingest.py                 # Downloads datasets & builds the SQLite databases
├── tools/
│   ├── db_tools.py           # SQL tools: hospitals, institutions, restaurants
│   └── web_search_tool.py    # Web search tool (SerpAPI) for general questions
├── requirements.txt          # Python dependencies
├── .env.example               # Template for your API keys
└── .gitignore                 # Files/folders kept out of Git (secrets, DBs, venv)
```

## 🏗️ How It Works (High-Level)

```
User question
     │
     ▼
 agent.py  ──►  LLM decides which tool fits the question
     │
     ├──► Hospitals SQL tool ──► dbs/hospitals.db
     ├──► Institutions SQL tool ──► dbs/institutions.db
     ├──► Restaurants SQL tool ──► dbs/restaurants.db
     └──► Web search tool ──► SerpAPI (general knowledge)
     │
     ▼
  Final answer
```

- **`ingest.py`** downloads each dataset from HuggingFace, cleans up the column names (lowercase, special characters → underscores, duplicates de-duplicated), and saves it as a table in a local SQLite `.db` file.
- **`tools/db_tools.py`** wraps each database as a LangChain-compatible tool that can run SQL queries and return results.
- **`tools/web_search_tool.py`** wraps SerpAPI so the agent can search the web when a question falls outside the datasets.
- **`agent.py`** wires the LLM and all the tools together into one agent that picks the right tool automatically.

### 📊 Datasets used

| Dataset (HuggingFace) | Local table |
|---|---|
| `Mahadih534/Institutional-Information-of-Bangladesh` | `institutions` |
| `Mahadih534/all-bangladeshi-hospitals` | `hospitals` |
| `Mahadih534/Bangladeshi-Restaurant-Data` | `restaurants` |

Want to add another dataset? Just add a `save_dataset_to_db(dataset_name, table_name, db_path)` call in `ingest.py`.

---

## 🚀 Getting Started

### 1. Clone & enter the project
```bash
git clone https://github.com/delowarhossaincse63/bd_multi_tool_ai_agent.git
cd bd_multi_tool_ai_agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API keys
```bash
copy .env.example .env        # Windows
cp .env.example .env          # macOS / Linux
```
Then open `.env` and fill in:
```
OPENAI_API_KEY=your_openai_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

### 5. Build the databases
```bash
python ingest.py
```
This creates:
- `dbs/hospitals.db`
- `dbs/institutions.db`
- `dbs/restaurants.db`

### 6. Run the agent
Interactive mode:
```bash
python agent.py
```
Or ask a direct question:
```bash
python agent.py "How many hospitals are in Dhaka?"
```

---

## 🔍 Quick Database Checks

Using the `sqlite3` CLI:
```bash
sqlite3 dbs/hospitals.db "PRAGMA table_info('hospitals');"
sqlite3 dbs/hospitals.db "SELECT COUNT(*) FROM hospitals;"
```

Or in Python:
```python
import sqlite3
conn = sqlite3.connect('dbs/hospitals.db')
cur = conn.cursor()
print(cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
print(cur.execute("SELECT count(*) FROM hospitals;").fetchone())
conn.close()
```

---

## 🛡️ What to Keep Out of GitHub

These are already excluded by `.gitignore` — never commit them:
- `.env` (your API keys)
- `dbs/*.db` (generated database files)
- `venv/` or `.venv/` (virtual environment)
- `__pycache__/` and `.pyc` files

**If you ever accidentally commit a secret**, don't just push a fix on top — remove it from history:
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git commit --amend --no-edit
git push -f origin main
```

---

## 🧯 Troubleshooting

| Problem | Fix |
|---|---|
| `OPENAI_API_KEY is required` | Make sure `.env` exists with the key set, then restart your terminal so it reloads. |
| GitHub blocks a push (secret detected) | Remove the secret from the file, amend/rebase the commit, then force-push. |
| Agent gives wrong/odd answers | Check the console for errors and confirm all required keys are in `.env`. |
| Web search doesn't work | Confirm `SERPAPI_API_KEY` is set — without it, the agent falls back to SQL tools only. |

---

## 🧪 Quick Test

```bash
python ingest.py
python agent.py "How many hospitals are in Dhaka?"
```

---

## 📬 Contact

**Delowar Hossain** — delowarhossain.cse.63@gmail.com

---

## 🏷️ Topics
`python` · `sqlite` · `langchain` · `huggingface` · `bangladesh` · `data-ingestion` · `web-search-agent`
