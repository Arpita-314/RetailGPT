# Architecture

This document describes the high-level data and training flow for the fine-tuning pipeline.

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

Brief explanation:

- Raw Dataset: Original data sources (JSONL, text, audio, etc.).
- ETL + Tokenizer: Cleaning, preprocessing, tokenization and sharding to Parquet for efficient IO.
- Distributed Trainer: Multi-GPU training using LoRA and optional DeepSpeed for memory optimization and speed.
- Quantized Model: Convert the fine-tuned weights to a low-bit representation (e.g., 4-bit) for efficient inference.
- Inference API (Ray): Serve model with Ray Serve (or FastAPI) for scalable inference.
- Monitoring Dashboard: Collect and visualize metrics like latency, throughput, and GPU utilization.
