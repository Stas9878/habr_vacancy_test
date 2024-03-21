from httpx import AsyncClient


async def test_add_rating(ac: AsyncClient ) -> None:
    for i in range(1, 3):
        response = await ac.post('/api/ratings/', json={
            'comics_id': 1,
            'user_id': i,
            'value': i * 2 #user1.rating = 2, user2.rating=4 (4 + 2) = 6
        })
        assert response.status_code == 200

async def test_get_rating(ac: AsyncClient) -> None:
    response = await ac.get('/api/comics/1/rating')
    
    assert response.status_code == 200
    
    data =  response.json()

    assert data['comics_id'] == 1
    assert data['title'] == 'TestComics'
    assert data['author'] == 'TestAuthor'
    assert data['rating'] == 3 #6 / 2 = 3  
    assert len(data) == 4