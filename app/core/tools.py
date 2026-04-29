import asyncio
import random
from langchain_core.tools import tool
from duckduckgo_search import DDGS  # Wapas normal DDGS import!


# 1. Ye normal sync helper function hai jisme hum DDGS chalayenge
def _run_sync_search(query: str):
    raw_results = []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        for r in results:
            raw_results.append(
                f"Title: {r.get('title', '')}\nInfo: {r.get('body', '')}"
            )
    return raw_results


# 2. Tera Asli Async Tool
@tool
async def web_search_tool(query: str) -> str:
    """
    Searches the web using DuckDuckGo to fetch the latest news, facts, and information about a specific topic.
    Always use this when you need current internet data.
    """
    print(f"🔍 Tool: Internet pe '{query}' search kar raha hun...")

    # JADOO 1: Random delay taaki DuckDuckGo hume block na kare (DDoS protection)
    await asyncio.sleep(random.uniform(0.5, 2.0))

    try:
        # JADOO 2: Hum normal Sync search ko background thread mein bhej rahe hain
        # Taaki LangGraph ka main loop hang na ho (Ctrl+C chalega!)
        raw_results = await asyncio.to_thread(_run_sync_search, query)

        if not raw_results:
            return "No search results found on the web."

        return "\n\n---\n\n".join(raw_results)

    except Exception as e:
        return f"Web search failed due to error: {str(e)}"
