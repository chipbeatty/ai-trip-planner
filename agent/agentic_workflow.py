from langgraph.graph import StateGraph
from typing import TypedDict, Optional
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import Runnable
from tools.weather_info_tool import get_weather
import asyncio
from agent.llm import extract_location_from_prompt

class AgentState(TypedDict):
    input: str
    location: Optional[str]
    weather: Optional[str]
    response: Optional[str]

# Step 2: Node to extract location (for now we hardcode)
"""
def extract_location(state: AgentState) -> AgentState:
    return {
            **state,
            "location": "Paris"
    }
"""

# Step 2: Node to extract location using openai
async def extract_location(state: AgentState) -> AgentState:
    prompt = state["input"]
    location = await extract_location_from_prompt(prompt)
    return {
        **state,
        "location": location
    }

# Step 3: Node to get weather info
async def fetch_weather(state: AgentState) -> AgentState:
    location = state["location"]
    weather = await get_weather(location)
    return {
        **state,
        "weather": weather
    }

# Step 4: Node to generate final message
def generate_response(state: AgentState) -> AgentState:
    return {
        **state,
        "response": f"Trip planned for {state["location"]}.\n{state["weather"]}"
    }

# Build the state graph
def build_trip_planner_graph() -> Runnable:
    builder = StateGraph(AgentState)

    builder.add_node("extract_location", extract_location)
    builder.add_node("fetch_weather", fetch_weather)
    builder.add_node("generate_response", generate_response)

    builder.set_entry_point("extract_location")
    builder.add_edge("extract_location", "fetch_weather")
    builder.add_edge("fetch_weather", "generate_response")
    builder.set_finish_point("generate_response")

    return builder.compile()


trip_graph = build_trip_planner_graph()

async def plan_trip(prompt: str) -> dict:
    result = await trip_graph.ainvoke({"input": prompt})
    return {"itinerary": result["response"]}

    
if __name__ == "__main__":
    prompt = "I want to travel to Paris next week."
    output = asyncio.run(plan_trip(prompt))
    print(output)
