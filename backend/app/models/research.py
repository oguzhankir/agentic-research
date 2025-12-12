from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Request/Response Models ---
class ResearchRequest(BaseModel):
    topic: str
    customization: Dict[str, Any] = {}

class ResearchResponse(BaseModel):
    research_id: str
    status: str
    message: str

# --- Domain Models ---
class ResearchQuestion(BaseModel):
    id: str = Field(description="Unique identifier for the question")
    question: str = Field(description="The specific research question")
    category: str = Field(description="Category: technical, business, market, news, etc.")
    priority: int = Field(description="Priority score 1-5 (5 is highest)")
    depth: str = Field(description="Expected depth: overview, deep-dive, fast-check")
    assigned_agent: str = Field(description="Agent responsible: web_researcher, technical_analyst, or business_analyst")

class ResearchPlan(BaseModel):
    questions: List[ResearchQuestion] = Field(description="List of research questions")
    estimated_time: str = Field(description="Estimated time to complete research")
