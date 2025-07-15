import asyncio
from agent.agentic_workflow import plan_trip

def main():
    prompt = "I want to visit Paris next week."
    result = asyncio.run(plan_trip(prompt))
    print("🌍 AI Trip Planner Output:")
    print(result["itinerary"])

if __name__ == "__main__":
    main()
