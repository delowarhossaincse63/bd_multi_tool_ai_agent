import sqlite3
from pathlib import Path
from typing import Dict, List

from langchain.tools import tool
from langchain_openai import ChatOpenAI


def _get_database_schema(db_path: Path) -> Dict[str, List[str]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    schema: Dict[str, List[str]] = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema[table] = [row[1] for row in cursor.fetchall()]
    conn.close()
    return schema


def _extract_sql(content: str) -> str:
    if "```" in content:
        chunks = content.split("```")
        if len(chunks) >= 2:
            content = chunks[1]
    return content.strip().rstrip(";").strip()


def _execute_sql(db_path: Path, sql: str) -> str:
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []

        if not rows:
            return "No rows were returned for that query."

        lines = []
        if columns:
            header = " | ".join(columns)
            lines.append(header)
            lines.append("-" * len(header))
        for row in rows[:20]:
            values = [str(value) if value is not None else "NULL" for value in row]
            lines.append(" | ".join(values))

        if len(rows) > 20:
            lines.append(f"...showing first 20 of {len(rows)} rows.")

        return "\n".join(lines)
    except sqlite3.Error as error:
        return f"SQL execution error: {error}"
    finally:
        conn.close()


def build_sql_tool(db_path: Path, name: str, description: str):
    schema = _get_database_schema(db_path)
    if not schema:
        raise ValueError(f"No tables found in database at {db_path}.")

    table_name = next(iter(schema))
    columns = schema[table_name]
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    schema_text = ", ".join(columns)

    @tool(name, description=description)
    def run_query(query: str) -> str:
        if not query or not query.strip():
            return "No question provided."

        prompt = (
            "You are a SQL generator for a SQLite database. "
            f"The database contains a table named '{table_name}' with columns: {schema_text}. "
            "Translate the user's question into a valid SQLite SELECT query. "
            "Return only the SQL query and nothing else. "
            "If the question cannot be answered with a SELECT query, return SELECT ''.\n\n"
            f"Question: {query}\nSQL:"
        )
        response = llm.invoke(prompt)
        sql = _extract_sql(getattr(response, "content", str(response)))
        if not sql.lower().startswith("select"):
            return "The generated SQL is not a SELECT statement. Please ask a question that can be answered with a SELECT query."
        return _execute_sql(db_path, sql)

    return run_query


def get_institutions_tool():
    db_path = Path(__file__).resolve().parent.parent / "dbs" / "institutions.db"
    return build_sql_tool(
        db_path=db_path,
        name="InstitutionsDBTool",
        description=(
            "Use this tool for questions about Bangladeshi institutions, universities, colleges, "
            "government organizations, and institution-specific data stored in the institutions database."
        ),
    )


def get_hospitals_tool():
    db_path = Path(__file__).resolve().parent.parent / "dbs" / "hospitals.db"
    return build_sql_tool(
        db_path=db_path,
        name="HospitalsDBTool",
        description=(
            "Use this tool for questions about Bangladeshi hospitals, beds, facilities, doctors, "
            "locations, and hospital-specific records stored in the hospitals database."
        ),
    )


def get_restaurants_tool():
    db_path = Path(__file__).resolve().parent.parent / "dbs" / "restaurants.db"
    return build_sql_tool(
        db_path=db_path,
        name="RestaurantsDBTool",
        description=(
            "Use this tool for questions about Bangladeshi restaurants, cuisine types, ratings, "
            "locations, and restaurant-specific records stored in the restaurants database."
        ),
    )
