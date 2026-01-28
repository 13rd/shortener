from src.service import generate_short_url
from tests.conftest import session


async def test_generate_short_url(session):  # not session==session
    result = await generate_short_url("https://example1.com", session)
    assert type(result) is str
    assert len(result) == 6