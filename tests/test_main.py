from fastapi.testclient import TestClient

from app.main import app, get_port

client = TestClient(app)


def test_root_says_hello():
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["project"] == "ok-to-keep-it"
    assert "hello" in body["message"]


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_get_port_reads_env(monkeypatch):
    monkeypatch.setenv("PORT", "1234")
    assert get_port() == 1234
    monkeypatch.delenv("PORT")
    assert get_port() == 8000
