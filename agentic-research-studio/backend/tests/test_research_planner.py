import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.agents.research_planner import ResearchPlannerAgent, ResearchPlan
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_research_planner_agent():
    # Mock the LLM
    mock_llm = MagicMock()
    
    # Mock the structured output return value
    # with_structured_output returns a Runnable, we need to mock that too
    mock_runnable = AsyncMock()
    mock_llm.with_structured_output.return_value = mock_runnable
    
    # Define what the runnable invokes returns
    mock_plan = ResearchPlan(
        questions=[
            {
                "id": "q1",
                "question": "What are the key security risks?",
                "category": "technical",
                "priority": 5,
                "depth": "deep-dive"
            }
        ],
        agent_assignments={"q1": "technical_analyst"},
        estimated_time="2 hours"
    )
    mock_runnable.invoke.return_value = mock_plan

    # Patch the ChatOpenAI instantiation in BaseAgent or ResearchPlannerAgent
    with patch("app.agents.base.ChatOpenAI", return_value=mock_llm):
        agent = ResearchPlannerAgent()
        
        initial_state: ResearchState = {
            "topic": "Quantum Computing",
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
        
        result_state = await agent.run_agent(initial_state)
        
        assert result_state["research_plan"] is not None
        plan = result_state["research_plan"]
        assert len(plan["questions"]) == 1
        assert plan["questions"][0]["id"] == "q1"
