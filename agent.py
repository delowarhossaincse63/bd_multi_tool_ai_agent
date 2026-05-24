import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools.db_tools import get_hospitals_tool, get_institutions_tool, get_restaurants_tool
from tools.web_search_tool import get_web_search_tool


def load_environment() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def build_agent():
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    tools = [
        get_hospitals_tool(),
        get_institutions_tool(),
        get_restaurants_tool(),
        get_web_search_tool(),
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        name="BangladeshAIAgent",
    )
    return agent


def format_agent_response(result) -> str:
    if hasattr(result, "output_text"):
        return result.output_text
    if hasattr(result, "content"):
        return result.content
    return str(result)


def main():
    load_environment()
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is required in the environment.")

    agent = build_agent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

    if not query:
        print("Enter a question for the Bangladesh AI Agent:")
        query = input("> ").strip()

    if not query:
        print("No query provided. Exiting.")
        return

    response = agent.invoke({"input": query})
    print("\n=== Agent response ===")
    print(format_agent_response(response))


if __name__ == "__main__":
    main()
