# Test-telegram-cmd

This is just to test the telegram command

Project code: `ok-to-keep-it` -- this is how Kaalsat refers to this project from
voice and Telegram ("how's ok-to-keep-it?", "ok-to-keep-it: run the tests").

This folder lives inside `agent-project/projects/`, so the top-level
`agent-project/CLAUDE.md` boundary rules apply here too.

## Status bookkeeping (required, every task)
- At the START of every task, set `STATUS.json` to
  `"status": "running"` with `"current_step"` describing the task.
- At the END, set `"status": "idle"` (or `"blocked"` / `"done"`), clear
  `"current_step"`, and write a one-paragraph `"last_completed_summary"`.
  Always refresh `"last_updated"` (ISO 8601, UTC).
- Then append one line to "Recent changes" below. Kaalsat reads
  `STATUS.json` directly to answer "what's happening?" without starting a
  session, so keep it truthful.

## Tech stack
- Backend: Python 3.12, FastAPI, uvicorn (ASGI server), pytest + httpx (tests).
- Frontend: React 18 + Vite 5 (plain JSX + CSS, no UI library) in `frontend/`.
- Why: the project only needs a small HTTP service that Kaalsat can build,
  test and deploy to Render. FastAPI is mainstream, has near-zero
  boilerplate, ships a test client, and Render's Python runtime runs it
  with a one-line start command. Vite is the mainstream React toolchain
  and its static build is trivially served by FastAPI.

## Architecture decisions
- Single module `app/main.py` holds the whole backend. The purpose is to
  test the Telegram command flow, so no layering, DB or auth.
- One Render service, not two: FastAPI serves `frontend/dist/index.html`
  at `/` and mounts `frontend/dist/assets` at `/assets`. The JSON hello
  moved to `/api/hello`. If the frontend is not built, `/` falls back to
  the JSON hello so tests and bare checkouts still work.
- `frontend/dist` is git-ignored; Render builds it (`npm ci && npm run
  build`) as part of the build command in `.kaalsat/deploy.json`. Render's
  Python runtime ships Node; `NODE_VERSION` can pin it.
- Vite dev server proxies `/api`, `/health*` to :8000 for local work.
- Background art is an in-repo SVG, not a downloaded photo: no licensing
  or external fetch, tiny (~3 KB), sharp at any viewport. Blended via a
  translucent warm gradient + `backdrop-filter` on the card so text stays
  readable.
- Config is env-vars only. `PORT` is read via `get_port()` (default 8000)
  so the same code runs locally and on Render, which injects `PORT`.
- `.env.example` documents every env var; there are no secrets yet. If one
  is added later, add its NAME to `.env.example` and read it with
  `os.environ` -- never hardcode values.
- Tests use FastAPI's in-process `TestClient`, so `pytest` needs no running
  server and no network.
- Deploy contract lives in `.kaalsat/deploy.json` (runtime `python`,
  `pip install -r requirements.txt`, `uvicorn ... --port $PORT`).

## How to run / test
- Setup: `python3 -m venv .venv && source .venv/bin/activate &&
  pip install -r requirements.txt`
- Frontend build: `npm --prefix frontend ci && npm --prefix frontend run build`
  (needs Node 22). Dev: `npm --prefix frontend run dev`.
- Run: `uvicorn app.main:app --reload --port 8000` (or `python -m app.main`,
  which honours `PORT`). Open `/` for the welcome page; `/api/hello`,
  `/api/version`, `/health`, `/healthz` for JSON.
- Test: `pytest` (7 tests, in-process, ~0.3s; pass with or without the
  frontend built). `pytest.ini` sets `pythonpath = .` so `app` imports.

## Key files
- `app/main.py` -- the FastAPI app: `/` (React page), `/api/hello`,
  `/api/version`, `/health`, `/healthz`, `/assets` mount, `get_port()`,
  `read_version()`.
- `VERSION` -- the app version (plain text, e.g. `0.1.0`); bump it here,
  `/api/version` reads it on every request.
- `pytest.ini` -- `pythonpath = .` and `testpaths = tests`.
- `frontend/src/App.jsx` -- the welcome page component (greeting, status
  pill fed by `/api/hello`, endpoint links).
- `frontend/src/index.css` -- warm palette, card, wave animation, sunrise
  background (gradient wash over the SVG, blurred glass card on top).
- `frontend/src/assets/sunrise.svg` -- hand-drawn sunrise illustration
  (sky gradient, sun + rays, layered hills); Vite inlines it into the CSS.
- `frontend/vite.config.js` -- React plugin, dev proxy, `dist` output.
- `tests/test_main.py` -- endpoint + PORT tests.
- `requirements.txt` -- pinned-range deps.
- `.kaalsat/deploy.json` -- Render build/start commands for Kaalsat.
- `.env.example` -- env var names (`PORT`, optional `NODE_VERSION`).
- `README.md` -- local run/test instructions.
- `STATUS.json` -- live status for Kaalsat (see bookkeeping above).

## Standing rules (apply to every session here)
- Boundary: only read, write or run things inside this folder (or elsewhere
  under `agent-project/`). Never touch anything outside it; if a task
  needs that, stop and explain instead.
- Privacy: never write, echo or repeat secrets, API keys, tokens, emails,
  usernames or other personal identifiers -- not in replies, code,
  comments, commits or docs. Secrets come from `.env` / environment
  variables only; `.env` is never committed.
- Git: do NOT run `git commit`, `git push`, `git init` or change branches.
  Kaalsat's bridge commits and pushes your work to `staging` after every
  task; `main` only moves via Kaalsat's `/promote ok-to-keep-it` command.
- Keep replies short and plain: they are read out loud or sent to Telegram.

## Conventions

## Recent changes (append-only, newest last)
- 2026-09-14: project registered with Kaalsat.
- 2026-09-14: scaffolded FastAPI service (app/main.py, tests, README,
  .gitignore, .env.example, .kaalsat/deploy.json); 3 tests passing.
- 2026-09-14: added GET /healthz returning {"ok": true} plus a test; 4 tests passing.
- 2026-09-14: added React/Vite welcome page in frontend/, served by FastAPI at /; hello JSON moved to /api/hello; Render build now also runs npm ci && npm run build; 5 tests passing.
- 2026-09-14: added blended sunrise SVG background to the welcome page (frontend/src/assets/sunrise.svg, index.css overlay/glass card); 5 tests passing.
- 2026-09-14: added GET /api/version reading the new VERSION file (0.1.0) plus two tests; added pytest.ini (pythonpath = .) so bare `pytest` works; 7 tests passing.
