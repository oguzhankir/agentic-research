from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_community.tools import DuckDuckGoSearchRun

class BusinessAnalystAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.search_tool = DuckDuckGoSearchRun()

    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Business Analyst: Analyzing market and business implications")
        
        research_plan = state.get("research_plan")
        if not research_plan:
            return state
            
        questions = research_plan.get("questions", [])
        
        # Filter questions assigned to business_analyst
        my_questions = [
            q for q in questions 
            if q.get("assigned_agent") == "business_analyst"
            or q.get("category") in ["business", "market", "industry"]
        ]
        
        # Remove duplicates
        seen_ids = set()
        unique_questions = []
        for q in my_questions:
            if q["id"] not in seen_ids:
                unique_questions.append(q)
                seen_ids.add(q["id"])
        
        if not unique_questions:
            logger.info("No business questions found.")
            return state

        findings = []
        
        for q in unique_questions:
            question_text = q["question"]
            # Enhance query for business focus
            search_query = f"{question_text} market size revenue trends business impact"
            logger.info(f"Business Research: {search_query}")
            
            try:
                state["progress_updates"].append(f"Business Analyst: Analyzing market data for {question_text}...")
                
                # Async search with timeout
                import asyncio
                results = await asyncio.wait_for(
                    asyncio.to_thread(self.search_tool.invoke, search_query),
                    timeout=15.0
                )
                
                # Use LLM to analyze the business findings
                analysis_prompt = f"""
                You are a Strategic Business Analyst (MBA/McKinsey style).
                Analyze these search results regarding: "{question_text}"
                
                Search Results:
                {results}
                
                Provide a strategic insight (SWOT, Market Size, CAGR, or Competitive Landscape).
                """
                
                analysis_response = await self.llm.ainvoke([HumanMessage(content=analysis_prompt)])
                analyzed_content = analysis_response.content
                
                findings.append({
                    "question_id": q["id"],
                    "question": question_text,
                    "content": analyzed_content,
                    "raw_content": results,
                    "source": "Business Analyst Agent",
                    "type": "market_analysis",
                    "url": "https://bloomberg.com" # Placeholder
                })
                
                state["progress_updates"].append(f"Business Insight generated: {question_text}")
                
            except Exception as e:
                logger.error(f"Error in Business Analyst for {question_text}: {e}")
                state["errors"].append(f"Business Analyst Error: {e}")

        current_findings = state.get("business_findings", [])
        state["business_findings"] = current_findings + findings
        state["progress_updates"].append("Business Analysis phase finished.")
        
        return state
