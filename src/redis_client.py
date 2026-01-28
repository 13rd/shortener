from redis.asyncio import Redis
from typing import Optional
import json
import pickle
from src.core.config import settings


class RedisClient:
    def __init__(self):
        self.client: Optional[Redis] = None

    async def connect(self):
        """initialize redis connection"""
        self.client = await Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db.cache,
        )

    async def disconnect(self):
        """clean up redis connection"""
        if self.client:
            await self.client.close()

    async def get(self, key: str, ) -> Optional[any]:
        """get value from redis cache"""
        try:
            data = await self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:  # custom error
            print("Error getting value from redis cache")


    async def set(self, key: str, value: any, expire: Optional[int] = None):
        """set value to redis cache"""
        try:
            json_value = json.dumps(value)
            if expire:
                await self.client.setex(key, expire, json_value)
            else:
                await self.client.set(key, json_value)
        except Exception as e:
            print("Error setting value to redis cache")

    async def delete(self, key: str):
        """delete value from redis cache"""
        try:
            await self.client.delete(key)
        except Exception as e:
            print("Error deleting value from redis cache")


    async def delete_pattern(self, pattern: str):
        """delete value from redis cache"""
        try:
            keys = await self.client.keys(pattern)
            if keys:
                await self.client.delete(*keys)
        except Exception as e:
            print("Error deleting value from redis cache")


redis_client = RedisClient()