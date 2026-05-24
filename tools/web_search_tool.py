import os
from typing import Dict

from langchain.tools import tool
from serpapi import GoogleSearch


def get_web_search_tool():
    @tool(
        "WebSearchTool",
        description=(
            "Use this tool for general knowledge questions, policy explanations, cultural context, "
            "and definitions about Bangladesh that are not directly available in the SQL databases."
        ),
    )
    def web_search(query: str) -> str:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError("SERPAPI_API_KEY is required in the environment.")

        params: Dict[str, str] = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": "5",
        }
        search = GoogleSearch(params)
        result = search.get_dict()

        organic = result.get("organic_results", [])
        if not organic:
            return "No web search results were found for that query."

        snippets = []
        for item in organic[:3]:
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No snippet available.")
            link = item.get("link", item.get("url", ""))
            snippets.append(f"{title}: {snippet} ({link})")

        return "\n".join(snippets)

    return web_search
