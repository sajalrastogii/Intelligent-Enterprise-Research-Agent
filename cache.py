import redis
import os
import json

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def get_cache(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cache(key, value):
    redis_client.set(key, json.dumps(value), ex=3600)
