import time
import threading
from typing import Dict, Any, Optional

class SimpleCache:
    def __init__(self, default_ttl: int = 15):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry["expires"]:
                    return entry["value"]
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl if ttl is not None else self.default_ttl
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires": time.time() + ttl
            }

    def invalidate_prefix(self, prefix: str) -> None:
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(prefix)]
            for k in keys_to_delete:
                del self._cache[k]

    def invalidate_all(self) -> None:
        with self._lock:
            self._cache.clear()

cache_service = SimpleCache(default_ttl=15)
