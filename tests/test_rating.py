from httpx import AsyncClient


async def test_add_rating(ac: AsyncClient ) -> None:
    response = await ac.post('/api/ratings/', json={
        'comics_id': 1,
        'user_id': 1,
        'value': 5
    })

    assert response.status_code == 200

async def test_get_rating(ac: AsyncClient) -> None:
    response = await ac.get('/api/comics/1/rating')
    
    assert response.status_code == 200
    
    data =  response.json()

    assert data['comics_id'] == 1
    assert data['title'] == 'TestComics'
    assert data['author'] == 'TestAuthor'
    assert data['rating'] == 5
    assert len(data) == 4