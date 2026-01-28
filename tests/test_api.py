from httpx import AsyncClient

async def test_short_url(ac: AsyncClient) -> None:
    result = await ac.post("/short_url", json={"long_url": "https://example.com"})
    assert result.status_code == 200
    assert "slug" in result.json()
    # result = await ac.get(f"/{result.json()['slug']}")
    # assert result.status_code == 302



async def test_redirect_to_url(ac: AsyncClient, created_short_url: str) -> None:
    slug = created_short_url
    result = await ac.get(f"/{slug}")
    assert result.status_code == 302
    assert result.headers["Location"] == f"https://example.com"