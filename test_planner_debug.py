import asyncio
import os
from dotenv import load_dotenv

# Force load .env from backend directory
load_dotenv("agentic-research-studio/backend/.env")

from app.agents.research_planner import ResearchPlannerAgent
from app.core.state import ResearchState

async def test_planner():
    print("Initializing Planner...")
    try:
        planner = ResearchPlannerAgent()
        print(f"Model: {planner.model_name}")
    except Exception as e:
        print(f"Failed to init: {e}")
        return

    state = {
        "topic": "Quantum Computing",
        "customization": {"depth": "basic", "tone": "professional"},
        "research_plan": None,
        "progress_updates": [],
        "errors": []
    }

    print("Running Planner...")
    try:
        new_state = await planner.invoke(state)
        print("Planner finished.")
        if new_state.get("research_plan"):
            print("Plan generated successfully:")
            print(new_state["research_plan"])
        else:
            print("No plan generated.")
            print("Errors:", new_state.get("errors"))
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_planner())
