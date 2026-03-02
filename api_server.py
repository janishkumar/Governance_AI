"""
FastAPI server for additional endpoints (roadmap generation)
Runs separately from LangGraph dev server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from app.roadmap import generate_roadmap

app = FastAPI(title="Career Coach API")

# CORS - UPDATED to allow your actual port
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5178",      # ← Add this (your actual port)
        "http://127.0.0.1:5178",      # ← Add this
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5181",
        "http://localhost:5182",
        "http://localhost:5183",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoadmapRequest(BaseModel):
    goal: str

@app.post("/generate-roadmap")
async def create_roadmap(request: RoadmapRequest):
    """Generate a career roadmap"""
    roadmap = generate_roadmap(request.goal)
    return {"roadmap": roadmap}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)