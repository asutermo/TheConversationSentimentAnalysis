import pytest

from TheConversationSentimentAnalysis.app.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_app() -> None:
    client = app.test_client()
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_index() -> None:
    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_about() -> None:
    test_client = app.test_client()
    response = await test_client.get("/about/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_404() -> None:
    test_client = app.test_client()
    response = await test_client.get("/nonexistentroute/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_article_with_valid_link() -> None:
    test_client = app.test_client()
    # Assuming 'example_title' and 'example_link' are valid for your application
    response = await test_client.get("/article/example_title?link=example_link")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_article_with_invalid_link() -> None:
    test_client = app.test_client()
    response = await test_client.get("/article/invalid_title")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ws_feed() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws/feed") as test_websocket:
        await test_websocket.receive()
