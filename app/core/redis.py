import redis.asyncio as redis
from app.core.config import Settings

settings = Settings()

redis_pool = redis.ConnectionPool.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)

async def get_redis():
    yield redis.Redis(connection_pool=redis_pool)