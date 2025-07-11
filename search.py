import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

@app.post("/search/")
async def search_handler(request: SearchRequest):
    query = request.query
    max_results = request.num_results

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": max_results
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(search_url, params=params)
            res.raise_for_status()
            data = res.json()
            snippets = [item.get("snippet", "") for item in data.get("items", [])]
            print("🔍 TNAU Search Snippets:", snippets)
            return {"snippets": snippets}
    except Exception as e:
        print("❌ TNAU Search Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
