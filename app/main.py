"""Test-telegram-cmd: a tiny FastAPI service used to exercise Kaalsat's Telegram command flow.

Serves the React welcome page (built into frontend/dist) at "/" and a few JSON
endpoints alongside it.

Configuration comes from environment variables only (see .env.example):
  PORT  - port the server binds to (Render sets this; defaults to 8000 locally).
"""

import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

APP_NAME = "Test-telegram-cmd"
PROJECT_CODE = "ok-to-keep-it"
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

app = FastAPI(title=APP_NAME)


def hello_payload() -> dict:
    return {"app": APP_NAME, "project": PROJECT_CODE, "message": "hello from ok-to-keep-it"}


@app.get("/api/hello")
def api_hello() -> dict:
    """JSON hello, consumed by the welcome page's status pill."""
    return hello_payload()


@app.get("/health")
def health() -> dict:
    """Health check used by Render and by Kaalsat status queries."""
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/healthz")
def healthz() -> dict:
    """Minimal liveness probe: always {"ok": true}, no timestamp."""
    return {"ok": True}


def frontend_built() -> bool:
    return (FRONTEND_DIST / "index.html").is_file()


@app.get("/")
def root():
    """The React welcome page when built; JSON hello otherwise (e.g. in tests)."""
    if frontend_built():
        return FileResponse(FRONTEND_DIST / "index.html")
    return hello_payload()


# Hashed JS/CSS bundles from `vite build`. Mounted after the routes above so
# the API and health endpoints always win.
if (FRONTEND_DIST / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


def get_port() -> int:
    """Port from the PORT env var, falling back to 8000 for local runs."""
    return int(os.environ.get("PORT", "8000"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=get_port())
