from httpx import AsyncClient


async def test_add_comics(ac: AsyncClient ) -> None:
    response = await ac.post('/api/add_comics/', json={
        'title': 'TestComics',
        'author': 'TestAuthor'
    })

    assert response.status_code == 200

async def test_get_comics(ac: AsyncClient) -> None:
    response = await ac.get('/api/comics/1/rating')
    
    assert response.status_code == 200
    
    data =  response.json()

    assert data['comics_id'] == 1

    assert data['title'] == 'TestComics'

    assert data['author'] == 'TestAuthor'

    assert len(data) == 4