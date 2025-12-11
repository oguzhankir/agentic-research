import pytest
from unittest.mock import MagicMock, patch
from app.agents.technical_analyst import TechnicalAnalystAgent
from app.agents.business_analyst import BusinessAnalystAgent
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_technical_analyst_agent():
    with patch("app.agents.technical_analyst.DuckDuckGoSearchRun") as MockSearch, \
         patch("app.agents.base.ChatOpenAI"):
        
        mock_search_instance = MockSearch.return_value
        mock_search_instance.invoke.return_value = "Technical docs and github repos"
        
        agent = TechnicalAnalystAgent()
        
        initial_state: ResearchState = {
            "topic": "Quantum Computing",
            "customization": {},
            "research_plan": {
                "questions": [
                    {"id": "q1", "question": "Qubit implementation", "category": "technical", "priority": 5, "depth": "deep-dive"},
                    {"id": "q2", "question": "Market size", "category": "business", "priority": 3, "depth": "overview"}
                ],
                "agent_assignments": {
                    "q1": "technical_analyst",
                    "q2": "business_analyst"
                },
                "estimated_time": "1 hour"
            },
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
        
        result_state = await agent.run_agent(initial_state)
        
        assert len(result_state["technical_findings"]) == 1
        finding = result_state["technical_findings"][0]
        assert finding["question_id"] == "q1"
        assert "documentation" in finding["raw_content"] or "Mocked" in finding["raw_content"] or "search results" in finding["raw_content"] or "Technical" in finding["raw_content"]


@pytest.mark.asyncio
async def test_business_analyst_agent():
    with patch("app.agents.business_analyst.DuckDuckGoSearchRun") as MockSearch, \
         patch("app.agents.base.ChatOpenAI"):
        
        mock_search_instance = MockSearch.return_value
        mock_search_instance.invoke.return_value = "Market size is $1B"
        
        agent = BusinessAnalystAgent()
        
        initial_state: ResearchState = {
            "topic": "Quantum Computing",
            "customization": {},
            "research_plan": {
                "questions": [
                    {"id": "q1", "question": "Qubit implementation", "category": "technical", "priority": 5, "depth": "deep-dive"},
                    {"id": "q2", "question": "Market size", "category": "business", "priority": 3, "depth": "overview"}
                ],
                "agent_assignments": {
                    "q1": "technical_analyst",
                    "q2": "business_analyst"
                },
                "estimated_time": "1 hour"
            },
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
        
        result_state = await agent.run_agent(initial_state)
        
        assert len(result_state["business_findings"]) == 1
        finding = result_state["business_findings"][0]
        assert finding["question_id"] == "q2"
        assert "Market size" in finding["raw_content"]
