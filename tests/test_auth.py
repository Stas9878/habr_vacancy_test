import pytest
from sqlalchemy import insert, select

from src.auth.models import User
from conftest import client, async_session_maker

def test_register():
    response = client.post('/auth/register', json={
        'email': 'test@mail.ru',
        'password': 'string',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'testname',
        })
    assert response.status_code == 201