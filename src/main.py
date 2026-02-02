from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from starlette import status
from src.core.config import settings
from src.exceptions import NonexistentUrlException, SlugAlreadyExistsException, InvalidUrlException
from src.database.db import engine, new_session
from src.database.models import Base
from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from src.service import generate_short_url, get_url_by_slug
from src.redis_client import redis_client, RedisClient


async def get_redis_client():
    return redis_client


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await redis_client.connect()
    yield
    await redis_client.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"])

@app.post("/short_url")
async def short_url(
        session: Annotated[AsyncSession, Depends(get_session)],
        long_url: Annotated[str, Body(embed=True)]
):
    try:
        new_slug = await generate_short_url(long_url, session=session)
        return {"slug": new_slug}
    except InvalidUrlException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid URL.")
    except SlugAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Slug not generated",
                            )


@app.get("/{slug}")
async def redirect_to_url(slug: str,
                          redis: Annotated[RedisClient, Depends(get_redis_client)],
                          session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        cached_url = await redis.get(slug)
        if cached_url:
            return RedirectResponse(url=cached_url, status_code=status.HTTP_302_FOUND)
        url = await get_url_by_slug(slug, session=session)
        await redis.set(slug, url, settings.cache.ttl_slug)
    except NonexistentUrlException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



"""
!ограничитель запросов
валидация url(бывают ссылки в приложениях, например tg://)
! создание человекочитаемых кастомных ссылок
аналитика переходов
время жизни ссылки
redis?
логи
генериция заранее
select for update
генерация не рандомно, а на основе ссылки?
несуществующие не определяет

обработка коллизий слагов(решено в 5 ретраев)

база данных для тестов
инверсия зависимостей, обёртка над сессией бд, свой класс

"""