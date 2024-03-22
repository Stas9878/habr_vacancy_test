import pytest
from conftest import client
from httpx import AsyncClient

#Тест регистрации юзера
def test_register() -> None:
    #Создаём 2 пользователя
    for i in range(1, 3):
        response = client.post('/auth/register', json={
            'email': f'test{i}@mail.ru',
            'password': 'string',
            'is_active': True,
            'is_superuser': False,
            'is_verified': False,
            'username': f'testname{i}',
            })
        
        assert response.status_code == 201


#Тест аутентификации юзеров
async def test_login(ac: AsyncClient) -> None:
    #Аутентифицируем 2-х пользователя
    for i in range(1, 3):
        response = await ac.post('/auth/login', data={
            'username': f'test{i}@mail.ru',
            'password': 'string',
            })

        assert response.status_code == 204