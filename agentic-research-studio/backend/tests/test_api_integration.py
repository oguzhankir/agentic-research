from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

client = TestClient(app)

def test_get_research_state():
    # 1. Start a research to get an ID
    with patch("app.main.BackgroundTasks.add_task") as mock_add_task:
        response = client.post(
            "/research",
            json={"topic": "Test Poll", "customization": {}}
        )
        assert response.status_code == 200
        data = response.json()
        research_id = data["research_id"]
        
    # 2. Poll the state
    response = client.get(f"/research/{research_id}")
    assert response.status_code == 200
    state = response.json()
    
    assert state["topic"] == "Test Poll"
    assert state["status"] == "started"
    assert state["metadata"]["research_id"] == research_id
    assert "progress_updates" in state

def test_get_research_state_not_found():
    response = client.get("/research/non-existent-id")
    assert response.status_code == 404
