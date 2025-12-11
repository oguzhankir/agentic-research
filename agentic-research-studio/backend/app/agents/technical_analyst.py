from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_community.tools import DuckDuckGoSearchRun

class TechnicalAnalystAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.search_tool = DuckDuckGoSearchRun()

    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Technical Analyst: Deep diving into technical aspects")
        
        research_plan = state.get("research_plan")
        if not research_plan:
            return state
            
        questions = research_plan.get("questions", [])
        
        # Filter questions assigned to technical_analyst
        my_questions = [
            q for q in questions 
            if q.get("assigned_agent") == "technical_analyst"
            or q.get("category") == "technical"
        ]
        
        # Remove duplicates if any
        seen_ids = set()
        unique_questions = []
        for q in my_questions:
            if q["id"] not in seen_ids:
                unique_questions.append(q)
                seen_ids.add(q["id"])
        
        if not unique_questions:
            logger.info("No technical questions found.")
            return state

        findings = []
        
        for q in unique_questions:
            question_text = q["question"]
            # Enhance query for technical focus
            search_query = f"{question_text} documentation github technical whitepaper"
            logger.info(f"Technical Research: {search_query}")
            
            try:
                results = self.search_tool.invoke(search_query)
                
                # Use LLM to analyze the technical findings
                analysis_prompt = f"""
                You are a Senior Technical Analyst. 
                Analyze these search results regarding: "{question_text}"
                
                Search Results:
                {results}
                
                Provide a concise technical deep-dive (2-3 paragraphs). Focus on architecture, stack, specs, and engineering details.
                """
                
                analysis_response = await self.llm.ainvoke([HumanMessage(content=analysis_prompt)])
                analyzed_content = analysis_response.content
                
                findings.append({
                    "question_id": q["id"],
                    "question": question_text,
                    "content": analyzed_content, # Analyzed output
                    "raw_content": results,
                    "source": "Technical Analyst Agent",
                    "type": "technical_deep_dive",
                    "url": "https://github.com" # Fallback for UI visualization
                })
                
                state["progress_updates"].append(f"Analyzed technical aspect: {question_text}")
                
            except Exception as e:
                logger.error(f"Error in Technical Analyst for {question_text}: {e}")
                state["errors"].append(f"Technical Analyst Error: {e}")

        current_findings = state.get("technical_findings", [])
        state["technical_findings"] = current_findings + findings
        
        return state
