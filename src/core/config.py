from pydantic import BaseModel
from redis.asyncio import Redis


class Config:
    ...

class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 6432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    driver: str = "asyncpg"

    pool_size: int = 20
    max_overflow: int = 30


class LoggingConfig(BaseModel):
    ...


class RedisDB(BaseModel):
    cache: int = 0

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()

class CacheConfig(BaseModel):
    prefix: str = "fastapi_cache"
    ttl_slug: int = 300


class Settings():
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()



settings = Settings()