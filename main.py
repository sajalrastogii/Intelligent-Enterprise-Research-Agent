import openai
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from cache import get_cache, set_cache
from metrics import REQUEST_COUNT, LATENCY
from prometheus_client import generate_latest
from sentence_transformers import SentenceTransformer
from time import time

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/metrics")
def metrics():
    return generate_latest()

async def stream_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        if "choices" in chunk:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]

@app.post("/query")
async def query_system(query: str):
    REQUEST_COUNT.inc()
    start = time()

    cached = get_cache(query)
    if cached:
        return cached

    prompt = f"Answer this question clearly: {query}"

    response = StreamingResponse(stream_response(prompt), media_type="text/plain")

    LATENCY.observe(time() - start)
    set_cache(query, {"status": "streaming"})

    return response
