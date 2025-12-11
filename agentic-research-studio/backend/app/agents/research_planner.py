from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger

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

class ResearchPlannerAgent(BaseAgent):
    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Research Planner: Generating research plan")
        
        topic = state["topic"]
        customization = state.get("customization", {})
        
        system_prompt = f"""You are an elite Research Strategist for the Agentic Research Studio.
        Your goal is to break down a user's research topic into a comprehensive, structured research plan.
        
        Topic: {topic}
        
        Customization Preferences:
        - Depth: {customization.get('depth', 'standard')}
        - Focus Areas: {', '.join(customization.get('focus_areas', []))}
        - Target Audience: {customization.get('target_audience', 'general')}
        
        Instructions:
        1. Analyze the topic complexity and scope.
        2. Generate 5-8 specific, high-value research questions that cover different angles (technical, business, recent news).
        3. Prioritize these questions based on the user's focus areas.
        4. For each question, assign it to the most appropriate agent using the 'assigned_agent' field:
           - 'technical_analyst' for implementation details, code, architecture, specs.
           - 'business_analyst' for market trends, companies, financials, impact.
           - 'web_researcher' for general news, recent events, broad overviews.
        5. Ensure questions are specific enough to yield good search results.
        """
        
        # Using with_structured_output to get Pydantic object directly
        structured_llm = self.llm.with_structured_output(ResearchPlan)
        
        try:
            plan: ResearchPlan = await structured_llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Create a research plan for: {topic}")
            ])
            
            # Convert Pydantic model to dict for state
            state["research_plan"] = plan.model_dump()
            state["progress_updates"].append(f"Research plan created with {len(plan.questions)} questions.")
            
        except Exception as e:
            logger.error(f"Error in Research Planner: {e}")
            state["errors"].append(f"Research Planner Error: {e}")
            # Fallback or re-raise could be implemented here
            
        return state
