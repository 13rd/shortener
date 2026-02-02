from src.service import generate_short_url, validate_url
from tests.conftest import session
import pytest
from src.exceptions import InvalidUrlException

async def test_generate_short_url(session):  # not session==session
    result = await generate_short_url("https://example1.com", session)
    assert type(result) is str
    assert len(result) == 6

async def test_invalid_url():
    with pytest.raises(InvalidUrlException):
        await validate_url("example1.com")

    result = await validate_url("  https://example1.com  ")
    assert result is True
