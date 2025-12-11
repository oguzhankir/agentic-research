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
                results = self.search_tool.invoke(search_query)
                
                # Use LLM to analyze the business findings
                analysis_prompt = f"""
                You are a Strategic Business Analyst. 
                Analyze these search results regarding: "{question_text}"
                
                Search Results:
                {results}
                
                Provide a strategic business assessment (2-3 paragraphs). Focus on market size, revenue, competitors, and growth potential.
                """
                
                analysis_response = await self.llm.ainvoke([HumanMessage(content=analysis_prompt)])
                analyzed_content = analysis_response.content
                
                findings.append({
                    "question_id": q["id"],
                    "question": question_text,
                    "content": analyzed_content,
                    "raw_content": results,
                    "source": "Business Analyst Agent",
                    "type": "business_analysis",
                    "url": "https://bloomberg.com" # Fallback/Placeholder for UI
                })
                
                state["progress_updates"].append(f"Analyzed business aspect: {question_text}")
                
            except Exception as e:
                logger.error(f"Error in Business Analyst for {question_text}: {e}")
                state["errors"].append(f"Business Analyst Error: {e}")

        current_findings = state.get("business_findings", [])
        state["business_findings"] = current_findings + findings
        
        return state
