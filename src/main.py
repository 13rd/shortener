from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from starlette import status
from src.exceptions import NonexistentUrlException, SlugAlreadyExistsException
from src.database.db import engine, new_session
from src.database.models import Base
from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from src.service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    ...

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

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
    except SlugAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Slug not generated",
                            )


@app.get("/{slug}")
async def redirect_to_url(slug: str,
                          session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        url = await get_url_by_slug(slug, session=session)
    except NonexistentUrlException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



"""
валидация url(бывают ссылки в приложениях, например tg://)
создание человекочитаемых кастомных ссылок
аналитика переходов
обработка коллизий слагов
время жизни ссылки
redis?
логи
генериция заранее
select for update
генерация не рандомно, а на основе ссылки?
несуществующие не определяет

база данных для тестов
инверсия зависимостей, обёртка над сессией бд, свой класс

"""