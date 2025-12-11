from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from app.core.config import settings, logger
from app.core.state import ResearchState
from app.core.graph import build_research_graph

app = FastAPI(
    title="Agentic Research Studio API",
    description="API for Agentic Research Studio",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Graph
research_graph = build_research_graph()

class ResearchRequest(BaseModel):
    topic: str
    customization: Dict[str, Any] = {}

class ResearchResponse(BaseModel):
    research_id: str
    status: str
    message: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

# In-memory store for MVP
RESEARCH_STORE = {}

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    import uuid
    research_id = str(uuid.uuid4())
    
    # Initialize state
    initial_state: ResearchState = {
        "topic": request.topic,
        "customization": request.customization,
        "research_plan": None,
        "web_findings": [],
        "technical_findings": [],
        "business_findings": [],
        "synthesized_content": None,
        "html_output": None,
        "quality_report": None,
        "status": "started",
        "progress_updates": ["Research started"],
        "errors": [],
        "metadata": {"research_id": research_id}
    }
    
    # Save to store
    RESEARCH_STORE[research_id] = initial_state

    # For now, we'll run it synchronously for the MVP proof or use background tasks if asyncio
    # Ideally, we should store the state in a DB or memory to retrieve later.
    
    async def run_graph(state, r_id):
        logger.info(f"Running graph for {state['topic']}")
        try:
            # invoke returns the final state
            final_state = await research_graph.ainvoke(state)
            logger.info("Graph execution completed")
            # Update store with final state
            RESEARCH_STORE[r_id] = final_state
        except Exception as e:
            logger.error(f"Graph execution failed: {e}")
            # Update store with error
            if r_id in RESEARCH_STORE:
                RESEARCH_STORE[r_id]["errors"].append(str(e))
                RESEARCH_STORE[r_id]["status"] = "error"

    background_tasks.add_task(run_graph, initial_state, research_id)

    return {
        "research_id": research_id,
        "status": "started",
        "message": "Research started in background"
    }

@app.get("/research/{research_id}")
async def get_research_status(research_id: str):
    state = RESEARCH_STORE.get(research_id)
    if not state:
        raise HTTPException(status_code=404, detail="Research not found")
    
    # Return relevant parts or full state
    return state

