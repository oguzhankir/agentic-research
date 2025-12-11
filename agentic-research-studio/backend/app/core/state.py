from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel

class ResearchState(TypedDict):
    topic: str
    customization: Dict[str, Any]
    research_plan: Optional[Dict[str, Any]]
    web_findings: List[Dict[str, Any]]
    technical_findings: List[Dict[str, Any]]
    business_findings: List[Dict[str, Any]]
    synthesized_content: Optional[Dict[str, Any]]
    html_output: Optional[str]
    quality_report: Optional[Dict[str, Any]]
    status: str
    progress_updates: List[str]
    errors: List[str]
    metadata: Dict[str, Any]
