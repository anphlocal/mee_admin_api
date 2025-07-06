import aioredis
from fastapi import Depends

from app.core.config import settings

class RedisCache:
    def __init__(self, url: str = settings.redis_url):
        self.url = url
        self.redis = None

    async def get_redis(self):
        if not self.redis:
            self.redis = await aioredis.from_url(self.url, decode_responses=True)
        return self.redis

redis_cache = RedisCache()
