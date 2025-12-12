from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_core.messages import SystemMessage, HumanMessage

class QualityReviewerAgent(BaseAgent):
    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Quality Reviewer: assessing content quality")
        
        content_to_review = state.get("synthesized_content")
        if not content_to_review:
            logger.warning("No synthesized content to review.")
            return state

        # Construct prompt
        system_prompt = """You are an Expert Editor and Fact Checker.
        Your goal is to review the provided research report for quality, clarity, and completeness.
        
        Criteria:
        1. Clarity and Readability: Is the language clear and easy to understand?
        2. Depth: Does it cover the topic sufficiently based on the gathered findings?
        3. Structure: Is the report well-structured (Executive Summary, Details, Takeaways)?
        
        Output Format:
        Return a simple evaluation text that includes:
        - Score: 1-10
        - Critique: A brief paragraph of feedback.
        - Status: PASS or IMPROVE
        """
        
        human_prompt = f"""Review the following report:
        
        {content_to_review}
        """
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            review_output = response.content
            state["quality_report"] = review_output
            state["progress_updates"].append(f"Quality Review Completed.")
            
            # Retrieve score from text if needed, for now just logging it.
            logger.info(f"Quality Review Report: {review_output[:100]}...")
            
        except Exception as e:
            logger.error(f"Error reviewing content: {e}")
            state["errors"].append(f"Quality Review Error: {e}")
            
        return state
