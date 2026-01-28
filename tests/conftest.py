from httpx import AsyncClient, ASGITransport
from pygments.styles.dracula import yellow

from src.database.models import Base
from src.main import app, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(url="sqlite+aiosqlite:///./test.db")

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session



app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with new_session() as session:
        yield session



@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac




@pytest.fixture(scope="function")
async def created_short_url(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "https://example.com"})
    # assert result.status_code == 200
    data = result.json()
    return data["slug"]