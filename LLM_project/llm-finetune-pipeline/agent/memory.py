"""Lightweight session memory for agent-like context.
Simple in-memory store with TTL. Replace with Redis or similar for production.
"""

import time
from typing import Dict, Any, Optional


class SessionMemory:
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def _prune(self) -> None:
        now = time.time()
        keys_to_delete = [k for k, v in self._store.items() if v["expires_at"] <= now]
        for k in keys_to_delete:
            del self._store[k]

    def set(self, session_id: str, data: Any) -> None:
        self._store[session_id] = {"value": data, "expires_at": time.time() + self.ttl}

    def get(self, session_id: str) -> Optional[Any]:
        self._prune()
        item = self._store.get(session_id)
        return item["value"] if item else None

    def append(self, session_id: str, datum: Any) -> None:
        current = self.get(session_id)
        if current is None:
            current = []
        current.append(datum)
        self.set(session_id, current)


# Quick smoke test
if __name__ == '__main__':
    m = SessionMemory(ttl_seconds=2)
    m.set('s1', ['hello'])
    print(m.get('s1'))
    time.sleep(3)
    print(m.get('s1'))
