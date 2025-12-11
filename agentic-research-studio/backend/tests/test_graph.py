import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.graph import build_research_graph
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_research_graph():
    # Define standalone async functions
    async def mock_planner_run(state: dict):
         return {"research_plan": {"questions": ["q1"]}}
         
    async def mock_web_run(state: dict):
        return {"web_findings": [{"id": "f1"}]}
        
    async def mock_tech_run(state: dict):
         return {"technical_findings": []}
         
    async def mock_biz_run(state: dict):
         return {"business_findings": []}

    # Mock all agents
    with patch("app.core.graph.ResearchPlannerAgent") as MockPlanner, \
         patch("app.core.graph.WebResearcherAgent") as MockWeb, \
         patch("app.core.graph.TechnicalAnalystAgent") as MockTech, \
         patch("app.core.graph.BusinessAnalystAgent") as MockBiz:
         
        # Configure mocks to return instances whose run_agent is our async function
        MockPlanner.return_value.run_agent = mock_planner_run
        MockWeb.return_value.run_agent = mock_web_run
        MockTech.return_value.run_agent = mock_tech_run
        MockBiz.return_value.run_agent = mock_biz_run
        
        graph = build_research_graph()
        
        initial_state: ResearchState = {
            "topic": "Test Topic",
            "customization": {},
            "research_plan": None,
            "web_findings": [],
            "technical_findings": [],
            "business_findings": [],
            "synthesized_content": None,
            "html_output": None,
            "quality_report": None,
            "status": "started",
            "progress_updates": [],
            "errors": [],
            "metadata": {}
        }
        
        # execute
        result = await graph.ainvoke(initial_state)
        
        assert result is not None
        # Check if updates were merged
        assert result.get("research_plan") == {"questions": ["q1"]}
        assert result.get("web_findings") == [{"id": "f1"}]
