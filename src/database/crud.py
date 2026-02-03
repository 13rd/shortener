# class Repository():
#     def __init__(self):
# from database.db import new_session
from datetime import timedelta, datetime, timezone
from operator import and_
from typing import Optional

from pendulum import UTC
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortUrl
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError

from src.exceptions import SlugAlreadyExistsException, ExpiredUrlException


async def add_slug_to_database(
        slug: str, long_url: str, session: AsyncSession, ttl: Optional[timedelta] = None,
):

    expires_at = datetime.now(timezone.utc) + ttl if ttl else None
    new_slug = ShortUrl(slug=slug, long_url=long_url, expires_at=expires_at)
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsException




async def get_url_from_database(
        slug: str, session: AsyncSession,
) -> str | None:
    query = select(ShortUrl).where(ShortUrl.slug == slug)
    result = await session.execute(query)
    short_url: ShortUrl | None = result.scalar_one_or_none()

    if not short_url:
        return None

    if short_url.expires_at is not None and short_url.expires_at <= datetime.now(timezone.utc):
        raise ExpiredUrlException

    return short_url.long_url

    # query = select(ShortUrl).where(
    #     ShortUrl.slug == slug,
    #     or_(
    #         ShortUrl.expires_at.is_(None),
    #         ShortUrl.expires_at > func.now()
    #     )
    # )
    # result = await session.execute(query)
    # res: ShortUrl | None = result.scalar_one_or_none()
    # return res.long_url if res else None
