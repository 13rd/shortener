from src.database.crud import add_slug_to_database, get_url_from_database
from src.exceptions import NonexistentUrlException, InvalidUrlException
from src.shortener import generate_random_slug
from src.exceptions import SlugAlreadyExistsException
from sqlalchemy.ext.asyncio import AsyncSession
import re


URL_PATTERN = re.compile(
    r'^(https?|ftp)://'
    r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
    r'[a-zA-Z]{2,}'
    r'(?::\d{1,5})?'
    r'(?:/[^\s]*)?$',
    re.IGNORECASE
)


async def validate_url(url: str) -> bool:
    """ Checks if the given url exists in the database
        :raises InvalidUrlException:
        :return: bool
    """
    if not url or not isinstance(url, str):
        raise InvalidUrlException()

    if not URL_PATTERN.match(url.strip()):
        raise InvalidUrlException()

    return True



async def generate_short_url(long_url: str, session: AsyncSession) -> str:
    """
    Generate a short slug, add in database and return it. Retry in 5 times if the slug already exists.
    #TODO: ПЕРЕДЕЛАТЬ
    :param long_url:
    :return:
    """
    #Если база данных вернула ошибку что slug уже существует, пробуем 5 раз генерировать

    await validate_url(long_url)

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
