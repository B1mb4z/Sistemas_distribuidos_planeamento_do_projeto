import pytest

from monolitico.server import server

def cliente():
    server.config['TESTING'] = True
    with server.test_client() as cliente:
        yield cliente

def test_get_items_empty(cliente):
    response = cliente.get('/itens')
    assert response.status_code == 200
    assert response.json == []

def test_add_item(cliente):
    response = cliente.post('/itens', json={'nome': 'Laptop'})
    assert response.status_code == 201
    assert response.json['nome'] == 'Laptop'

def test_add_order(cliente):
    # First add an item (optional, but for demo)
    cliente.post('/itens', json={'nome': 'Mouse'})
    response = cliente.post('/pedidos', json={'item_id': 1, 'quantidade': 2})
    assert response.status_code == 201
    assert response.json['item_id'] == 1