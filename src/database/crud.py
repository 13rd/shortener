# class Repository():
#     def __init__(self):
# from database.db import new_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortUrl
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.exceptions import SlugAlreadyExistsException


async def add_slug_to_database(
        slug: str, long_url: str, session: AsyncSession,
):

     new_slug = ShortUrl(slug=slug, long_url=long_url)
     session.add(new_slug)
     try:
        await session.commit()
     except IntegrityError:
        raise SlugAlreadyExistsException




async def get_url_from_database(
        slug: str, session: AsyncSession,
) -> str | None:

    query = select(ShortUrl).filter_by(slug=slug)
    result = await session.execute(query)
    res: ShortUrl | None = result.scalar_one_or_none()
    return res.long_url if res else None
