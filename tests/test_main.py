from fastapi.testclient import TestClient

from app.main import app, frontend_built, get_port

client = TestClient(app)


def test_api_hello():
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    body = resp.json()
    assert body["project"] == "ok-to-keep-it"
    assert "hello" in body["message"]


def test_root_serves_page_or_json():
    resp = client.get("/")
    assert resp.status_code == 200
    if frontend_built():
        assert "text/html" in resp.headers["content-type"]
        assert "<div id=\"root\">" in resp.text
    else:
        assert resp.json()["project"] == "ok-to-keep-it"


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_healthz_returns_ok_true():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_get_port_reads_env(monkeypatch):
    monkeypatch.setenv("PORT", "1234")
    assert get_port() == 1234
    monkeypatch.delenv("PORT")
    assert get_port() == 8000
