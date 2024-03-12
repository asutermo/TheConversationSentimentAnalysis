import pytest

from ..app.app import app


@pytest.mark.asyncio
async def test_index():
    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_about():
    test_client = app.test_client()
    response = await test_client.get("/about/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_404():
    test_client = app.test_client()
    response = await test_client.get("/nonexistentroute/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_article_with_valid_link():
    test_client = app.test_client()
    # Assuming 'example_title' and 'example_link' are valid for your application
    response = await test_client.get("/article/example_title?link=example_link")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_article_with_invalid_link():
    test_client = app.test_client()
    response = await test_client.get("/article/invalid_title")
    assert response.status_code == 404
