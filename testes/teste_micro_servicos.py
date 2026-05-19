import pytest
import requests

BASE_URL = 'http://localhost:5000'  # API Gateway dos microserviços

def test_items_flow():
    # POST /itens
    resp = requests.post(f'{BASE_URL}/itens', json={'nome': 'Keyboard'})
    assert resp.status_code == 201
    assert resp.json()['nome'] == 'Keyboard'

    # GET /itens
    resp = requests.get(f'{BASE_URL}/itens')
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert any(item['nome'] == 'Keyboard' for item in resp.json())

def test_orders_flow():
    # POST /pedidos
    resp = requests.post(f'{BASE_URL}/pedidos', json={'item_id': 1, 'quantidade': 5})
    assert resp.status_code == 201
    assert resp.json()['quantidade'] == 5

    # GET /pedidos
    resp = requests.get(f'{BASE_URL}/pedidos')
    assert resp.status_code == 200
    assert len(resp.json()) >= 1