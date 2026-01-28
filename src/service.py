from src.database.crud import add_slug_to_database, get_url_from_database
from src.exceptions import NonexistentUrlException
from src.shortener import generate_random_slug
from src.exceptions import SlugAlreadyExistsException
from sqlalchemy.ext.asyncio import AsyncSession


async def generate_short_url(long_url: str, session: AsyncSession) -> str:
    """
    Generate a short slug, add in database and return it. Retry in 5 times if the slug already exists.
    #TODO: ПЕРЕДЕЛАТЬ
    :param long_url:
    :return:
    """
    #Если база данных вернула ошибку что slug уже существует, пробуем 5 раз генерировать

    async def _generate_slug_and_add_to_database() -> str:
        generated_slug = generate_random_slug()
        await add_slug_to_database(generated_slug, long_url, session=session)
        return generated_slug

    for attempt in range(5):
        try:
            generated_slug = await _generate_slug_and_add_to_database()
            return generated_slug
        except SlugAlreadyExistsException:
            if attempt == 4:
                raise SlugAlreadyExistsException()





async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    url = await get_url_from_database(slug, session=session)
    if not url:
        raise NonexistentUrlException()
    return url
