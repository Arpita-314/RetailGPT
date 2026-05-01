"""Tokenization, batching, and caching helpers for the inference server."""


def batch_requests(requests, batch_size: int = 8):
    for i in range(0, len(requests), batch_size):
        yield requests[i:i+batch_size]
