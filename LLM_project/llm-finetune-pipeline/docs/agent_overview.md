# Domain-Adaptive Text Agent — Overview

This document gives a short overview of the Domain-Adaptive Text Agent: goals, components, and quick usage.

Goals
- Demonstrate data readiness (ETL + sharded Parquet) for scalable fine-tuning.
- Run domain-adaptive fine-tuning on modern transformer encoders (DeBERTa/RoBERTa) with experiment tracking.
- Provide a small session-memory layer to allow short-term context for multi-turn agent dialogues.
- Expose a fast inference API with batching and simple caching for low-latency responses.
- Hook basic monitoring and reproducibility (W&B / MLflow placeholders).

Components
- `data_pipeline/` — ETL and tokenizer utilities. Output: sharded Parquet + pre-tokenized datasets.
- `training/` — Training entry points, experiment helpers, and configs. Use this for running distributed jobs.
- `agent/` — Minimal session memory and agent orchestration helpers.
- `inference/` — FastAPI/Ray Serve server code and batching utilities.
- `monitoring/` — Metrics collection and dashboard code (Streamlit/Grafana placeholders).

Quick start (developer)
1. Prepare data in `data_pipeline/` using the ETL utilities.
2. Configure fine-tuning in `training/trainer_config.yaml`.
3. Start the training script (use `scripts/train_distributed.sh` as a template).
4. After training, run `inference/app.py` to serve the model and test via the `/generate` endpoint.

Next steps
- Add example dataset and a small end-to-end notebook that goes from raw data -> trained model -> served inference.
- Wire up W&B/MLflow for experiment logging.
