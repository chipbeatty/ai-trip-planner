import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import plan_trip

"""FastAPI recommends using a Pydantic model to define request schemas. This way:

Swagger UI shows a proper input box with a prompt field

You get automatic data validation"""

#use for hardcoded testing
"""def main():
    prompt = "I want to visit Paris next week."
    result = asyncio.run(plan_trip(prompt))
    print("🌍 AI Trip Planner Output:")
    print(result["itinerary"])"""

app = FastAPI()

# Allow CORS for Streamlit frontend or testing tools like Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    prompt: str

@app.post("/plan")
async def plan(request: TripRequest):
    result = await plan_trip(request.prompt)
    return result

if __name__ == "__main__":
 #   main() Use for hardcoded testing
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
