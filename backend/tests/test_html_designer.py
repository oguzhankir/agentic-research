import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.html_designer import HTMLDesignerAgent
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_html_designer_agent():
    with patch("app.agents.base.ChatOpenAI") as MockLLM:
        mock_llm_instance = MockLLM.return_value
        mock_llm_instance.ainvoke = AsyncMock(return_value=MagicMock(content="<!DOCTYPE html><html><body>Report</body></html>"))
        
        agent = HTMLDesignerAgent()
        
        initial_state: ResearchState = {
            "topic": "Test",
            "customization": {},
            "research_plan": None,
            "web_findings": [],
            "technical_findings": [],
            "business_findings": [],
            "synthesized_content": "# Report Header\nContent",
            "html_output": None,
            "quality_report": None,
            "status": "started",
            "progress_updates": [],
            "errors": [],
            "metadata": {}
        }
        
        result_state = await agent.run_agent(initial_state)
        
        assert result_state["html_output"] is not None
        assert "<!DOCTYPE html>" in result_state["html_output"]
        assert "HTML Report generated." in result_state["progress_updates"]
