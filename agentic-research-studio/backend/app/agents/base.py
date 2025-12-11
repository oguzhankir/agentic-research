from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings, logger
from app.core.state import ResearchState

class BaseAgent(ABC):
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.OPENAI_MODEL_NAME
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7
        )

    @abstractmethod
    async def invoke(self, state: ResearchState) -> ResearchState:
        """
        Main method to execute the agent's logic.
        Must be implemented by all subclasses.
        """
        pass

    async def run_agent(self, state: ResearchState) -> ResearchState:
        """
        Wrapper method to handle logging and error management.
        """
        agent_name = self.__class__.__name__
        logger.info(f"Starting execution of {agent_name}")
        
        try:
            result = await self.invoke(state)
            logger.info(f"Constructed new state from {agent_name}")
            return result
        except Exception as e:
            logger.error(f"Error in {agent_name}: {str(e)}")
            state["errors"].append(f"{agent_name}: {str(e)}")
            state["status"] = "failed"
            return state
