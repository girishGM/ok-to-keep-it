# Test-telegram-cmd

Project code: `ok-to-keep-it`

A small FastAPI service that serves a warm React welcome page and a few JSON
endpoints. It exists to give Kaalsat's Telegram command flow something real
to build, test and deploy.

| Route          | Purpose                                            |
|----------------|----------------------------------------------------|
| `GET /`        | React welcome page (JSON hello if not built)       |
| `GET /api/hello` | Hello JSON with the project code                 |
| `GET /health`  | Health check (`{"status": "ok", ...}`)             |
| `GET /healthz` | Minimal liveness probe (`{"ok": true}`)            |

## Requirements

- Python 3.12 (3.10+ should work)
- Node.js 22 + npm (to build the frontend)

## Run locally

```bash
# backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# frontend (one-off build; FastAPI serves frontend/dist at /)
npm --prefix frontend ci
npm --prefix frontend run build

cp .env.example .env        # optional; only sets PORT
uvicorn app.main:app --reload --port 8000
```

Then open <http://localhost:8000/>.

For live-reload frontend work run `npm --prefix frontend run dev` in a second
terminal and open the Vite URL it prints; it proxies `/api`, `/health` and
`/healthz` to the FastAPI server on :8000.

## Test

```bash
pytest
```

Tests pass with or without the frontend built.

## Configuration

All configuration comes from environment variables (see `.env.example`).
Never commit `.env`.

| Variable       | Default | Meaning                                              |
|----------------|---------|------------------------------------------------------|
| `PORT`         | `8000`  | Port the server binds to; Render sets it.            |
| `NODE_VERSION` | Render default | Node used by Render's build step (optional).  |

## Deploy

`.kaalsat/deploy.json` describes the build and start commands Kaalsat uses
for the Render web service. The build installs Python deps, then runs
`npm ci && npm run build` in `frontend/`; the start command binds to `$PORT`.
