"""Placeholder wrapper for experiment tracking (W&B / MLflow).
Swap in real W&B or MLflow APIs when ready.
"""


def log_metrics(metrics: dict, step: int = None):
    print(f"[W&B placeholder] step={step} metrics={metrics}")


def log_artifact(path: str, name: str = None):
    print(f"[W&B placeholder] save artifact {path} as {name}")
