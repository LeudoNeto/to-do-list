import redis
import os

CACHE_TTL = 60 * 5

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

REDIS_HOST = REDIS_URL.split("//")[1].split(":")[0]
REDIS_PORT = REDIS_URL.split(":")[2].split("/")[0]
REDIS_DB = REDIS_URL.split("/")[3]

redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def delete_get_all_cache(redis_cache: redis.Redis, model: str):
    for key in redis_cache.scan_iter(f"{model}:all*"):
        redis_cache.delete(key)
