from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any, List
import uuid

from app.core.config import logger
from app.core.state import ResearchState
from app.core.graph import build_research_graph
from app.core.store import RESEARCH_STORE
from app.models.research import ResearchRequest, ResearchResponse

router = APIRouter()

# Initialize Graph
research_graph = build_research_graph()

@router.post("", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
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

@router.get("/{research_id}")
async def get_research_status(research_id: str):
    state = RESEARCH_STORE.get(research_id)
    if not state:
        raise HTTPException(status_code=404, detail="Research not found")
    
    # Return relevant parts or full state
    return state
