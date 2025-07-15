import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def extract_location_from_prompt(prompt: str) -> str:
    system_prompt = (
        "You are a helpful AI assistant that extracts the destination city "
        "from a user's travel prompt. Only return the city name."
    )
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    location = response.choices[0].message.content.strip()
    return location