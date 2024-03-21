import pytest
from conftest import client

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