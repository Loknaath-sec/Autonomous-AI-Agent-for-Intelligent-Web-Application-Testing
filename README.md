# Autonomous AI Agent for Intelligent Web Application Testing

Autonomous AI Agent for Intelligent Web Application Testing is a research-oriented autonomous web testing platform that converts a natural-language testing instruction and target URL into a structured execution loop combining multi-agent planning, hybrid perception, Playwright automation, selector healing, independent verification, long-horizon exploration, memory, and evidence-based bug reporting.

## Research problem

Current autonomous web agents can navigate pages but often misinterpret outcomes, confuse automation failures with website defects, struggle with selector drift, and do not produce strong evidence-backed bug reports. This autonomous AI agent addresses that gap by combining multi-agent reasoning, hybrid perception, self-healing recovery, verification, and research instrumentation.

## Research gap and contributions

This project builds on the research direction in web agents and web probing but focuses on the practical testing problem: reducing false positives, managing long-horizon exploration, preserving execution memory, and generating reproducible evidence.

Contributions include:
- Multi-agent architecture for planning, perception, execution, verification, bug analysis, and reporting
- Hybrid web perception combining DOM, accessibility, text, screenshots, and browser metadata
- Self-healing selectors with structured confidence tracking
- Independent verification to reduce false positives
- Long-horizon exploration with bounded depth and step controls
- Persistent memory for prior workflows and bug patterns
- Research dashboards and experiment tracking for reproducible evaluation

## Architecture summary

- Backend: FastAPI + SQLAlchemy + Playwright
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Database: SQLite for development, PostgreSQL for production
- AI provider: OpenAI-compatible abstraction with validation and safe parsing
- Deployment: Docker and Render-friendly configuration

## Local setup

1. Create a Python environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Install the Playwright browser binaries:
   python -m playwright install chromium
4. Create a frontend environment:
   cd frontend
   npm install
5. Copy environment variables:
   cp .env.example .env

### Python path for local development

The backend package is under the `backend` folder. When running tests or local scripts from the repo root, set `PYTHONPATH=backend` or use the included pytest configuration.

## Running locally

Backend:
- cd backend
- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Frontend:
- cd frontend
- npm run dev -- --host 0.0.0.0

Demo site:
- cd demo-site
- python -m http.server 8001

## Research experiments

The project includes baseline and proposed-mode comparison utilities, plus experiment tracking. Run:
- pytest
- python scripts/run_experiments.py

## Deployment

The repo includes a Dockerfile, docker-compose.yml, and render.yaml for Render deployment. Production uses PostgreSQL. Local development defaults to SQLite.

## Ethical considerations

This autonomous testing system should only test websites the user owns or has explicit permission to test. The system blocks destructive actions, credential attacks, and unauthorized access paths.

## Limitations

- Local storage is suitable for demos; production should use object storage or external report storage.
- LLM reasoning remains dependent on API availability and model quality.
- Browser automation can still be impacted by anti-bot protections and dynamic UI frameworks.

## Future work

- Add richer visual QA and OCR pipelines
- Add event streaming to the live execution UI
- Expand experiment benchmarks and comparison baselines
- Add more browser engines and accessibility scanning rules

