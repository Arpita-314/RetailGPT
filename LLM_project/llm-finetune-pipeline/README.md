# Domain-Adaptive Text Agent

A production-minded MLOps + Applied-ML project: **Domain-Adaptive Text Agent** that demonstrates
data readiness (ETL), domain fine-tuning, a lightweight agent context/memory layer, and a deployable inference API.

This repo is built to showcase:
- Scalable ETL and sharded dataset storage
- Fine-tuning modern transformers (DeBERTa/RoBERTa) with experiment tracking
- Lightweight session memory for agent-like context
- FastAPI inference server with batching and simple caching
- Monitoring and reproducibility hooks (W&B / MLflow placeholders)

---

## Quick repo layout

llm-finetune-pipeline/
│
├── data_pipeline/        # ETL, tokenizer, sharding to Parquet
├── agent/                # Lightweight session memory and agent helpers
├── training/             # Training scripts, experiment code, configs
├── inference/            # FastAPI/Ray Serve application + serving utils
├── monitoring/           # Metrics collection and dashboard placeholders
├── scripts/              # Useful shell helpers (download, train, run)
├── tests/                # Unit tests and lightweight integration tests
├── docker/               # Dockerfile(s) and compose for local dev
└── docs/                 # Architecture and design docs

See `docs/` for architecture and `docs/agent_overview.md` for agent specifics.

## Architecture

```
		   +--------------------+
		   |   Raw Dataset      |
		   +--------+-----------+
					|
					v
		   +--------------------+
		   |   ETL + Tokenizer  |
		   | (sharded Parquet)  |
		   +--------+-----------+
					|
					v
		   +--------------------+
		   | Distributed Trainer|
		   |  (LoRA/DeepSpeed)  |
		   +--------+-----------+
					|
					v
		   +--------------------+
		   | Quantized Model    |
		   | (4-bit inference)  |
		   +--------+-----------+
					|
					v
		   +--------------------+
		   | Inference API (Ray)|
		   +--------+-----------+
					|
					v
		   +--------------------+
		   | Monitoring Dashboard|
		   +--------+-----------+
```
