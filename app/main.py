"""Test-telegram-cmd: a tiny FastAPI service used to exercise Kaalsat's Telegram command flow.

Configuration comes from environment variables only (see .env.example):
  PORT  - port the server binds to (Render sets this; defaults to 8000 locally).
"""

import os
from datetime import datetime, timezone

from fastapi import FastAPI

APP_NAME = "Test-telegram-cmd"
PROJECT_CODE = "ok-to-keep-it"

app = FastAPI(title=APP_NAME)


@app.get("/")
def root() -> dict:
    """Simple hello endpoint so a Telegram command has something to poke."""
    return {"app": APP_NAME, "project": PROJECT_CODE, "message": "hello from ok-to-keep-it"}


@app.get("/health")
def health() -> dict:
    """Health check used by Render and by Kaalsat status queries."""
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/healthz")
def healthz() -> dict:
    """Minimal liveness probe: always {"ok": true}, no timestamp."""
    return {"ok": True}


def get_port() -> int:
    """Port from the PORT env var, falling back to 8000 for local runs."""
    return int(os.environ.get("PORT", "8000"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=get_port())
