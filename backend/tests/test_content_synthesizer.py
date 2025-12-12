import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.content_synthesizer import ContentSynthesizerAgent
from app.core.state import ResearchState

@pytest.mark.asyncio
async def test_content_synthesizer_agent():
    # Mock ChatOpenAI
    with patch("app.agents.base.ChatOpenAI") as MockLLM:
        mock_llm_instance = MockLLM.return_value
        mock_llm_instance.ainvoke = AsyncMock(return_value=MagicMock(content="# Research Report\n\nExisting content"))
        
        agent = ContentSynthesizerAgent()
        
        initial_state: ResearchState = {
            "topic": "Quantum Computing",
            "customization": {"tone": "academic"},
            "research_plan": None,
            "web_findings": [{"question": "What is it?", "raw_content": "A type of computing."}],
            "technical_findings": [{"question": "How does it work?", "raw_content": "Qubits."}],
            "business_findings": [{"question": "Market size?", "raw_content": "Big."}],
            "synthesized_content": None,
            "html_output": None,
            "quality_report": None,
            "status": "started",
            "progress_updates": [],
            "errors": [],
            "metadata": {}
        }
        
        result_state = await agent.run_agent(initial_state)
        
        assert result_state["synthesized_content"] is not None
        assert "# Research Report" in result_state["synthesized_content"]
        assert "Research content synthesized." in result_state["progress_updates"]
