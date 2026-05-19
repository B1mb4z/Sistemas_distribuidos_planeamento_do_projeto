import pytest
from monolitico import server  # server.py na mesma pasta/raiz do projeto

@pytest.fixture
def cliente():
    server.config['TESTING'] = True
    with server.test_client() as c:
        yield c

def test_get_items_empty(cliente):
    response = cliente.get('/itens')
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_item(cliente):
    response = cliente.post('/itens', json={'nome': 'Laptop'})
    assert response.status_code == 201
    assert response.get_json()['nome'] == 'Laptop'

def test_add_order(cliente):
    cliente.post('/itens', json={'nome': 'Mouse'})
    response = cliente.post('/pedidos', json={'item_id': 1, 'quantidade': 2})
    assert response.status_code == 201
    assert response.get_json()['item_id'] == 1