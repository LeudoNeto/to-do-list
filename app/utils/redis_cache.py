import redis
import os

CACHE_TTL = 60 * 5

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def delete_get_all_cache(redis_cache: redis.Redis, model: str):
    for key in redis_cache.scan_iter(f"{model}:all*"):
        redis_cache.delete(key)
