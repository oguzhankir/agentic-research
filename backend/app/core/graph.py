from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from app.core.state import ResearchState
from app.agents.research_planner import ResearchPlannerAgent
from app.agents.web_researcher import WebResearcherAgent
from app.agents.technical_analyst import TechnicalAnalystAgent
from app.agents.business_analyst import BusinessAnalystAgent
from app.agents.content_synthesizer import ContentSynthesizerAgent
from app.agents.html_designer import HTMLDesignerAgent
from app.agents.quality_reviewer import QualityReviewerAgent
from app.core.config import logger

def build_research_graph():
    # Initialize agents
    planner = ResearchPlannerAgent()
    web_researcher = WebResearcherAgent()
    technical_analyst = TechnicalAnalystAgent()
    business_analyst = BusinessAnalystAgent()
    content_synthesizer = ContentSynthesizerAgent()
    quality_reviewer = QualityReviewerAgent()
    html_designer = HTMLDesignerAgent()

    # Define the graph
    workflow = StateGraph(ResearchState)

    # Add nodes - Wrap in RunnableLambda to ensure async handling
    workflow.add_node("research_planner", RunnableLambda(planner.run_agent))
    workflow.add_node("web_researcher", RunnableLambda(web_researcher.run_agent))
    workflow.add_node("technical_analyst", RunnableLambda(technical_analyst.run_agent))
    workflow.add_node("business_analyst", RunnableLambda(business_analyst.run_agent))
    workflow.add_node("content_synthesizer", RunnableLambda(content_synthesizer.run_agent))
    workflow.add_node("quality_reviewer", RunnableLambda(quality_reviewer.run_agent))
    workflow.add_node("html_designer", RunnableLambda(html_designer.run_agent))
    
    # Define edges - Linear Flow for Safety
    # Entry point
    workflow.set_entry_point("research_planner")

    # Linear chain
    workflow.add_edge("research_planner", "web_researcher")
    workflow.add_edge("web_researcher", "technical_analyst")
    # Execute analysts in parallel? For now linear for safety
    workflow.add_edge("technical_analyst", "business_analyst")
    workflow.add_edge("business_analyst", "content_synthesizer")
    workflow.add_edge("content_synthesizer", "quality_reviewer")
    workflow.add_edge("quality_reviewer", "html_designer")
    workflow.add_edge("html_designer", END)

    # Compile
    app = workflow.compile()
    return app
