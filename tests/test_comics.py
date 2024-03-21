from httpx import AsyncClient


#Тест добавления комикса
async def test_add_comics(ac: AsyncClient) -> None:
    #Делаем пост запрос для создания комикса
    response = await ac.post('/api/add_comics/', json={
        'title': 'TestComics',
        'author': 'TestAuthor'
    })

    assert response.status_code == 200

