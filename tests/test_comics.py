from httpx import AsyncClient


async def test_add_comics(ac: AsyncClient ) -> None:
    response = await ac.post('/api/add_comics/', json={
        'title': 'TestComics',
        'author': 'TestAuthor'
    })

    assert response.status_code == 200

