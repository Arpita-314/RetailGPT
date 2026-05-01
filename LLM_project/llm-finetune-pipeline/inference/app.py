"""Simple FastAPI inference server placeholder.
Use Ray Serve or FastAPI + Uvicorn as desired.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate(prompt: dict):
    # placeholder response
    return {"generated_text": "This is a placeholder."}
