import pytest
from conftest import client

def test_register() -> None:
    response = client.post('/auth/register', json={
        'email': 'test@mail.ru',
        'password': 'string',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'testname',
        })
    assert response.status_code == 201