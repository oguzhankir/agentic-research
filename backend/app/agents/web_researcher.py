from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
import json
from app.utils.text import clean_json_response
from app.models.research import ResearchPlan, ResearchQuestion

class WebResearcherAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        # Revert to simple SearchRun as requested by user
        self.search_tool = DuckDuckGoSearchRun() 

    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Web Researcher: Conducting research")
        state["progress_updates"].append("Web Researcher: Starting search process...")
        
        research_plan = state.get("research_plan")
        if not research_plan:
            logger.warning("No research plan found. Skipping web research.")
            return state
            
        questions = research_plan.get("questions", [])
        
        # Filter questions assigned to web_researcher
        my_questions = [
            q for q in questions 
            if q.get("assigned_agent") in ["web_researcher", "market_analyst"]
            or q.get("category") in ["market", "news", "general"]
        ]
        
        if not my_questions:
            logger.info("No questions assigned to Web Researcher.")
            state["progress_updates"].append("No specific web questions found.")
            return state

        findings = []
        state["progress_updates"].append(f"Identified {len(my_questions)} key questions to research.")
        
        for i, q in enumerate(my_questions):
            question_text = q["question"]
            logger.info(f"Researching: {question_text}")
            state["progress_updates"].append(f"Searching: {question_text}...")
            
            try:
                # Run synchronous search in a separate thread to prevent blocking
                # Add a 15-second timeout to prevent global hangs
                import asyncio
                search_results = await asyncio.wait_for(
                    asyncio.to_thread(self.search_tool.invoke, question_text),
                    timeout=15.0
                )
                
                # Basic parsing or just use the raw snippet
                findings.append({
                    "question_id": q["id"],
                    "question": question_text,
                    "raw_content": search_results,
                    "source": "DuckDuckGo",
                    "type": "web_search",
                    "url": "https://duckduckgo.com" # Placeholder as SearchRun doesn't return URL easily
                })
                
                state["progress_updates"].append(f"Found data for: {question_text}")
                
            except Exception as e:
                logger.error(f"Error searching for {question_text}: {e}")
                state["errors"].append(f"Web Search Error ({question_text}): {e}")

        # Update state with new findings
        current_findings = state.get("web_findings", [])
        state["web_findings"] = current_findings + findings
        
        state["progress_updates"].append("Web Research completed successfully.")
        return state
