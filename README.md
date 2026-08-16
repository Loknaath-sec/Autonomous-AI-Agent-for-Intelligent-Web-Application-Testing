# Autonomous AI Agent for Intelligent Web Application Testing
### Developed by:
#### Loknaath P (212223240080)
#### Lokhnath J (212223240079)




Modern, research-driven platform that converts a natural-language testing instruction and a target URL into a reproducible, evidence-backed test run. The system integrates multi-agent planning, hybrid perception, robust browser automation, selector self-healing, independent verification, and structured report generation.

Key outcomes: deterministic, instruction-specific reports; reproducible evidence artifacts; and a developer-friendly dashboard for experiments.

---

## Highlights (what makes this project important)

- **Natural-language driven** testing: provide a plain-English instruction and receive a full test run and HTML report.
- **Hybrid perception**: DOM + accessibility tree + textual analysis + browser metadata (noisy visual data optional).
- **Self-healing selectors**: resilient automation when selectors drift or DOM changes.
- **False-positive reduction**: independent verification layer distinguishes automation issues from real defects.
- **Evidence-based reporting**: structured reproduction steps, HTTP logs, and saved artifacts.
- **Reproducible experiments**: built-in experiment tracking and dashboards for research evaluation.

---

## Tech Stack (detailed)

- Backend: **Python**, **FastAPI**, **SQLAlchemy**, **Alembic** (migrations), **Playwright** (browser automation)
- Frontend: **React**, **TypeScript**, **Vite**, **Tailwind CSS**, **Recharts** (visualizations)
- Database: **SQLite** (local/dev), **PostgreSQL** (production-ready)
- Testing: **pytest**, FastAPI TestClient, Playwright test helpers
- LLM / AI: pluggable OpenAI-compatible provider abstraction (safe parsing + response validation)
- Storage: local `./reports` for dev; pluggable object storage (S3) recommended for production
- Infra / DevOps: **Docker**, **docker-compose**, **Render** config included
- CI: simple pytest steps (adapt for GitHub Actions / GitLab CI)

---

## Repository layout (key files)

- `backend/` – FastAPI application, agents, report generator, DB models, and scripts
- `frontend/` – React + TypeScript UI and dashboard
- `backend/reports/` – persisted HTML reports and saved artifacts
- `backend/scripts/` – dev utilities: `generate_samples.py`, `check_variation.py`
- `backend/tests/` – unit and integration tests
- `docker-compose.yml`, `Dockerfile`, `render.yaml` – deployment artifacts

---

## Quickstart — Local Development (tested)

Prereqs: Python 3.10+, Node 18+, npm/yarn, Git

1. Create and activate Python venv

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install backend deps

```powershell
pip install -r backend/requirements.txt
```

3. Install Playwright browsers

```powershell
python -m playwright install chromium
```

4. Start backend (development)

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8005
```

5. Start frontend (development)

```powershell
cd frontend
npm install
npm run dev
# frontend dev server runs on http://localhost:5173
```

Notes:
- The default `API_BASE_URL` used by the frontend should point to `http://localhost:8005` during development.
- When running tests or scripts from the repo root, the backend package can be importable by adding `backend` to `PYTHONPATH` or running scripts from inside `backend/`.

---

## Commands (tests, samples, build)

- Run backend tests: `python -m pytest backend/tests` 
- Generate sample reports: `python backend/scripts/generate_samples.py` 
- Quick variation check: `python backend/scripts/check_variation.py` 
- Build frontend (production): `cd frontend && npm run build`

---

## Deployment

- Docker-friendly: `docker-compose up --build` builds both backend and frontend; production uses `POSTGRES_URL` and external object storage.
- Render: `render.yaml` included with recommended runtime settings. Validate environment variables for API keys and DB connection first.

## Security & Ethics

- Only run tests against targets you own or have permission to test. This tool should never be used for unauthorized scanning.
- Sensitive credentials must be provided via secure environment variables and never committed to the repository.

---

## Contributing & Research

Contributions are welcome. For research reproducibility:

- Provide experiment config files and seed data.
- Add deterministic seeds for any stochastic agents.
- Commit datasets and experimental results when permitted.

### Recommended next steps for researchers

1. Swap the `AI provider` implementation to your preferred model and add test harnesses.
2. Extend the `ReportGenerator` with richer evidence attachments and custom templates.
3. Add CI steps to run experiments and collect metrics automatically.

---

## License

This repository uses an open-source friendly license (see `LICENSE` file). If you plan to use this for anything other than research, review the license and update deployment configurations accordingly.

---



