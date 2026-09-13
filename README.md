# Test-telegram-cmd

Project code: `ok-to-keep-it`

A tiny FastAPI web service whose only job is to give Kaalsat's Telegram
command flow something real to run, test and deploy. It exposes two JSON
endpoints:

| Route     | Purpose                                   |
|-----------|-------------------------------------------|
| `GET /`   | Hello message with the project code       |
| `GET /health` | Health check (`{"status": "ok", ...}`) |

## Requirements

- Python 3.12 (3.10+ should work)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # optional; only sets PORT
uvicorn app.main:app --reload --port 8000
```

Then open <http://localhost:8000/> or <http://localhost:8000/health>.

`python -m app.main` also works and reads `PORT` from the environment.

## Test

```bash
pytest
```

## Configuration

All configuration comes from environment variables (see `.env.example`).
Never commit `.env`.

| Variable | Default | Meaning                                   |
|----------|---------|-------------------------------------------|
| `PORT`   | `8000`  | Port the server binds to; Render sets it. |

## Deploy

`.kaalsat/deploy.json` describes the build and start commands Kaalsat uses
to create a Render web service. The start command binds to `$PORT`.
