from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from app.core.config import settings
from operator import add
from pydantic import BaseModel, Field
from langgraph.types import Send
from app.core.tools import web_search_tool
import asyncio


llm = init_chat_model(
    model="gpt-4o-mini", model_provider="openai", api_key=settings.OPENAI_API_KEY
)


# State classes
class OverAllState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    topics: list[str]
    all_report: Annotated[list[str], add]
    final_summary: str


class WorkerState(TypedDict):
    topic: str


# Structured output models
class TopicStructure(BaseModel):
    topics: list[str] = Field(description="List of topics to research")


# Structured llm
topic_llm = llm.with_structured_output(schema=TopicStructure)


# Nodes
async def manager_node(state: OverAllState) -> dict:
    user_query = state["messages"][-1]  # This is already a HumanMessage

    system_message = SystemMessage(
        content=f"""
You are a Lead Analyst. Break down the user's company analysis request into EXACTLY 3 specific web search queries.
Make sure the queries are optimized for a search engine.
"""
    )

    response: TopicStructure = await topic_llm.ainvoke([system_message, user_query])

    return {"topics": response.topics}


async def spawn_workers_parallel_routing_funciton(state: OverAllState):
    topics = state["topics"]

    tasks = []

    for topic in topics:
        tasks.append(Send(node="worker_node", arg={"topic": topic}))

    return tasks


async def worker_node(state: WorkerState) -> dict:
    topic = state["topic"]

    # 1. Tool chalaya
    raw_results = await web_search_tool.ainvoke({"query": topic})

    # JADOO YAHAN HAI (Humne Tag laga diya string ke upar)
    tagged_data = f"--- DATA FOR TOPIC: {topic} ---\n{raw_results}\n"

    # Ab tagged data append hoga
    return {"all_report": [tagged_data]}


async def reducer_node(state: OverAllState) -> OverAllState:
    # 1. Saare tagged reports ko ek sath jod liya
    combined_reports = "\n\n".join(state["all_report"])
    user_query = state["messages"][-1].content

    # 2. SYSTEM MESSAGE: Sirf rules
    system_message = SystemMessage(
        content="""You are a Lead Corporate Analyst. 
        Write a highly professional Executive Summary in Markdown. 
        Use headings, bullet points, and highlight key metrics. 
        ONLY use the provided data. Do not hallucinate."""
    )

    # 3. HUMAN MESSAGE: User ki query + Saara data yahan jayega!
    human_prompt = f"""
    The user wants an analysis on: '{user_query}'
    
    Here is the researched data from different departments:
    {combined_reports}
    
    Please generate the final report based on the data above.
    """

    response = await llm.ainvoke([system_message, HumanMessage(content=human_prompt)])

    return {"messages": [response], "final_summary": response.content}


# graph

graph = StateGraph(state_schema=OverAllState)

graph.add_node("manager_node", manager_node)
graph.add_node("worker_node", worker_node)
graph.add_node("reducer_node", reducer_node)


graph.add_edge(START, "manager_node")
graph.add_conditional_edges(
    "manager_node", spawn_workers_parallel_routing_funciton, ["worker_node"]
)
graph.add_edge("worker_node", "reducer_node")
graph.add_edge("reducer_node", END)

workflow = graph.compile()


async def run_agent(user_query: str) -> str:
    initial_state: OverAllState = {
        "messages": [HumanMessage(content=user_query)],
        "topics": [],
        "all_report": [],
        "final_summary": "",
    }

    final_state = await workflow.ainvoke(initial_state)
    print(final_state["final_summary"])


asyncio.run(run_agent("Analyse infosys"))
