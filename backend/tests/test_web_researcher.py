import pytest
from unittest.mock import MagicMock, patch
from app.agents.web_researcher import WebResearcherAgent
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_web_researcher_agent():
    # Mock DuckDuckGoSearchRun AND ChatOpenAI (from BaseAgent)
    with patch("app.agents.web_researcher.DuckDuckGoSearchRun") as MockSearch, \
         patch("app.agents.base.ChatOpenAI"):  # Patch ChatOpenAI to prevent validation/network errors
        
        mock_search_instance = MockSearch.return_value
        mock_search_instance.invoke.return_value = "Mocked search results for quantum computing"
        
        agent = WebResearcherAgent()
        
        # Prepare state with a research plan
        initial_state: ResearchState = {
            "topic": "Quantum Computing",
            "customization": {},
            "research_plan": {
                "questions": [
                    {
                        "id": "q1", 
                        "question": "What is quantum computing?", 
                        "category": "general",
                        "priority": 5,
                        "depth": "overview"
                    },
                    {
                        "id": "q2", 
                        "question": "Technical implementation of Qubits", 
                        "category": "technical",
                        "priority": 5,
                        "depth": "deep-dive"
                    }
                ],
                "agent_assignments": {
                    "q1": "web_researcher",
                    "q2": "technical_analyst"
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
        
        assert len(result_state["web_findings"]) == 1
        finding = result_state["web_findings"][0]
        assert finding["question_id"] == "q1"
        assert finding["raw_content"] == "Mocked search results for quantum computing"
        
        # Ensure q2 was NOT researched by this agent
        assert len([f for f in result_state["web_findings"] if f["question_id"] == "q2"]) == 0
