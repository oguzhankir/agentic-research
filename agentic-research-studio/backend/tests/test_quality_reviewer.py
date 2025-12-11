import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.quality_reviewer import QualityReviewerAgent
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_quality_reviewer_agent():
    with patch("app.agents.base.ChatOpenAI") as MockLLM:
        mock_llm_instance = MockLLM.return_value
        mock_llm_instance.ainvoke = AsyncMock(return_value=MagicMock(content="Score: 9\nCritique: Good.\nStatus: PASS"))
        
        agent = QualityReviewerAgent()
        
        initial_state: ResearchState = {
            "topic": "Test",
            "customization": {},
            "research_plan": None,
            "web_findings": [],
            "technical_findings": [],
            "business_findings": [],
            "synthesized_content": "# Report\nGood content.",
            "html_output": None,
            "quality_report": None,
            "status": "started",
            "progress_updates": [],
            "errors": [],
            "metadata": {}
        }
        
        result_state = await agent.run_agent(initial_state)
        
        assert result_state["quality_report"] is not None
        assert "Score: 9" in result_state["quality_report"]
        assert "Quality Review Completed." in result_state["progress_updates"]
