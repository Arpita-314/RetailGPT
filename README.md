# RetailGPT

> **AI-powered retail intelligence platform with integrated real-time fraud detection.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [FraudGuard Module](#fraudguard-module)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

RetailGPT is an end-to-end, production-ready platform that combines **Large Language Model (LLM) capabilities** with **machine-learning-based fraud detection** for modern retail operations. It exposes a unified REST API that enables downstream services and front-end applications to:

- Query natural-language retail analytics and insights powered by GPT-class models.
- Score transactions in real time using the embedded **FraudGuard** engine, which blends rule-based heuristics with trained ML classifiers.
- Ingest, transform, and serve retail feature data through a clean, schema-validated pipeline.

The system is designed for **horizontal scalability**, **observability**, and **CI/CD integration**, following the twelve-factor app methodology.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Clients                          │
│          (Web · Mobile · Internal Services)             │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS / REST
┌────────────────────────▼────────────────────────────────┐
│                      API Layer                          │
│   FastAPI  ·  Pydantic schemas  ·  Route handlers       │
│              api/routes/  ·  api/schemas/               │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
┌──────────▼──────────┐   ┌───────────▼───────────────────┐
│   LLM / GPT Engine  │   │        FraudGuard Engine       │
│  (Retail analytics, │   │  fraudguard/                  │
│   Q&A, forecasting) │   │  ├── data/      (ingestion)   │
└─────────────────────┘   │  ├── features/  (engineering) │
                          │  ├── models/    (ML scoring)  │
                          │  ├── rules/     (heuristics)  │
                          │  ├── serving/   (inference)   │
                          │  └── utils/     (helpers)     │
                          └───────────────────────────────┘
                                         │
                          ┌──────────────▼──────────────────┐
                          │     Config & Secrets Layer       │
                          │          config/                 │
                          └──────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---|---|
| **Retail AI Chat** | Natural-language interface to query sales data, inventory levels, and customer trends via GPT models. |
| **Real-Time Fraud Scoring** | Sub-100 ms transaction scoring combining rule engine and ML models. |
| **Feature Pipeline** | Automated feature extraction and transformation from raw retail events. |
| **Rule Engine** | Declarative, hot-reloadable business rules for fraud heuristics (velocity checks, geo-anomalies, etc.). |
| **Model Registry Integration** | Plug-in interface for MLflow / Vertex AI / SageMaker model artifacts. |
| **Schema Validation** | Request/response contracts enforced via Pydantic v2 schemas. |
| **Structured Logging** | JSON log output with correlation IDs compatible with ELK / Datadog. |
| **Health & Readiness Probes** | Kubernetes-ready `/healthz` and `/readyz` endpoints. |

---

## Repository Structure

```
RetailGPT/
├── api/                        # REST API layer (FastAPI)
│   ├── routes/                 # Endpoint definitions grouped by domain
│   └── schemas/                # Pydantic request/response models
├── config/                     # Application configuration (env-driven)
├── fraudguard/                 # FraudGuard fraud-detection subsystem
│   ├── data/                   # Data loaders & connectors
│   ├── features/               # Feature engineering pipelines
│   ├── models/                 # ML model wrappers & registry clients
│   ├── rules/                  # Rule-based detection engine
│   ├── serving/                # Inference server & batch scoring utilities
│   └── utils/                  # Shared helpers (logging, metrics, etc.)
├── .gitignore
└── README.md
```

---

## Prerequisites

| Dependency | Minimum Version | Notes |
|---|---|---|
| Python | 3.10 | 3.11+ recommended |
| pip / uv | latest | `uv` recommended for speed |
| Docker | 24.x | For containerised local dev |
| Docker Compose | 2.x | Local service orchestration |
| PostgreSQL | 14+ | Primary datastore |
| Redis | 7+ | Cache & rate-limiting backend |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Arpita-314/RetailGPT.git
cd RetailGPT
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or, using uv:
uv pip install -r requirements.txt
```

### 4. Install development extras (optional)

```bash
pip install -r requirements-dev.txt
pre-commit install
```

---

## Configuration

All runtime configuration is driven by **environment variables**. Copy the example file and populate it for your environment:

```bash
cp .env.example .env
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `APP_ENV` | Yes | `development` | `development` \| `staging` \| `production` |
| `OPENAI_API_KEY` | Yes | — | OpenAI API key for GPT inference |
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Redis connection string |
| `FRAUDGUARD_MODEL_URI` | No | — | URI of the trained fraud model artifact |
| `LOG_LEVEL` | No | `INFO` | `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` |
| `SECRET_KEY` | Yes | — | HMAC secret for JWT signing |
| `ALLOWED_ORIGINS` | No | `*` | Comma-separated CORS origins |

> **Security note:** Never commit `.env` to version control. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager) in production environments.

---

## Running the Application

### Local development server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The interactive API docs are available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Docker Compose (full stack)

```bash
docker compose up --build
```

This starts the API server, PostgreSQL, and Redis together. The API will be reachable at `http://localhost:8000`.

---

## API Reference

All endpoints are versioned under `/api/v1`.

### Health Checks

| Method | Path | Description |
|---|---|---|
| `GET` | `/healthz` | Liveness probe |
| `GET` | `/readyz` | Readiness probe (checks DB & Redis) |

### Retail Intelligence

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/chat` | Submit a natural-language retail query |
| `GET` | `/api/v1/insights/sales` | Sales trend analysis |
| `GET` | `/api/v1/insights/inventory` | Inventory anomaly detection |

### FraudGuard

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/fraud/score` | Score a single transaction |
| `POST` | `/api/v1/fraud/batch` | Batch-score up to 500 transactions |
| `GET` | `/api/v1/fraud/rules` | List active fraud rules |
| `PUT` | `/api/v1/fraud/rules/{rule_id}` | Enable / disable a rule |

Full OpenAPI spec is auto-generated and available at `/openapi.json`.

---

## FraudGuard Module

FraudGuard is a self-contained fraud-detection library embedded in the platform. It follows a **layered scoring** approach:

```
Raw Transaction
      │
      ▼
  data/         ← normalise & validate incoming event
      │
      ▼
  features/     ← derive velocity, geo, behavioural signals
      │
      ▼
  rules/        ← fast-path rule evaluation (allow / deny / review)
      │
      ▼
  models/       ← ML gradient-boosting / neural scorer
      │
      ▼
  serving/      ← aggregate score + explainability payload
```

### Score Response Schema

```json
{
  "transaction_id": "txn_abc123",
  "score": 0.87,
  "risk_level": "HIGH",
  "triggered_rules": ["VELOCITY_EXCEEDED", "GEO_MISMATCH"],
  "model_version": "v2.3.1",
  "latency_ms": 42
}
```

`risk_level` thresholds (configurable):

| Level | Score Range | Default Action |
|---|---|---|
| `LOW` | 0.00 – 0.39 | Allow |
| `MEDIUM` | 0.40 – 0.69 | Step-up authentication |
| `HIGH` | 0.70 – 0.89 | Hold for review |
| `CRITICAL` | 0.90 – 1.00 | Block |

---

## Development

### Code style

The project enforces consistent style using [Black](https://github.com/psf/black) and [isort](https://pydantic-docs.helpmanual.io/). Run the formatters before committing:

```bash
black .
isort .
```

### Linting

```bash
flake8 .
mypy .
```

### Pre-commit hooks

After running `pre-commit install`, hooks run automatically on `git commit`. To run them manually:

```bash
pre-commit run --all-files
```

---

## Testing

Tests are written with [pytest](https://pytest.org) and live alongside the source under `tests/`.

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run only fraud-detection tests
pytest tests/fraudguard/

# Run only API tests
pytest tests/api/
```

CI enforces a minimum coverage threshold of **80%**.

---

## Deployment

### Docker image

```bash
docker build -t retailgpt:latest .
docker run -p 8000:8000 --env-file .env retailgpt:latest
```

### Kubernetes

Helm chart and Kubernetes manifests are maintained in the `deploy/` directory (coming soon). Key resources:

- `Deployment` — stateless API pods with liveness/readiness probes.
- `HorizontalPodAutoscaler` — scales on CPU utilisation and custom RPS metrics.
- `ConfigMap` / `Secret` — injected via environment variables at pod start.

### Environment promotion

```
feature branch → staging (auto-deploy on PR merge) → production (manual approval gate)
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch: `git checkout -b feat/your-feature`.
2. Make your changes, ensuring all tests pass and linters are clean.
3. Open a **Pull Request** against `main` with a clear description of the change and its motivation.
4. A maintainer will review the PR. Addressed comments must be re-requested for review.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor guidelines and our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full text.

---

> Built with ❤️ by the RetailGPT team.
