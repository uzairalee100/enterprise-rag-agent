from fastapi.testclient import TestClient

from app.api import app
from app.agent import ask

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint(monkeypatch):
    def mock_ask(question):
        assert question == "What is the PTO policy?"

        return {
            "answer": "Employees receive 21 days of PTO per year.",
            "sources": ["pto_policy"],
        }

    monkeypatch.setattr("app.api.ask", mock_ask)

    response = client.post(
        "/chat",
        json={"question": "What is the PTO policy?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Employees receive 21 days of PTO per year.",
        "sources": ["pto_policy"],
    }


def test_chat_rejects_missing_question():
    response = client.post("/chat", json={})

    assert response.status_code == 422
