from sqlalchemy import insert, select

from conftest import client


# pytest tests -p no:warnings -v
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