from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger

class WebResearcherAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.search_tool = DuckDuckGoSearchRun()

    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Web Researcher: Conducting research")
        
        research_plan = state.get("research_plan")
        if not research_plan:
            logger.warning("No research plan found. Skipping web research.")
            return state
            
        questions = research_plan.get("questions", [])
        # assignments = research_plan.get("agent_assignments", {}) # Deprecated
        
        # Filter questions assigned to web_researcher
        my_questions = [
            q for q in questions 
            if q.get("assigned_agent") == "web_researcher"
        ]
        
        if not my_questions:
            logger.info("No questions assigned to Web Researcher.")
            return state

        findings = []
        
        for q in my_questions:
            question_text = q["question"]
            logger.info(f"Researching: {question_text}")
            
            try:
                # In a real scenario, we might use the LLM to generate better search queries
                # For now, we search the question directly
                search_results = self.search_tool.invoke(question_text)
                
                findings.append({
                    "question_id": q["id"],
                    "question": question_text,
                    "raw_content": search_results,
                    "source": "DuckDuckGo",
                    "type": "web_search"
                })
                
                state["progress_updates"].append(f"Researched: {question_text}")
                
            except Exception as e:
                logger.error(f"Error searching for {question_text}: {e}")
                state["errors"].append(f"Web Search Error ({question_text}): {e}")

        # Update state with new findings
        # We extend existing findings or create new list
        current_findings = state.get("web_findings", [])
        state["web_findings"] = current_findings + findings
        
        return state
