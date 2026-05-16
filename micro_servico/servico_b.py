# micro_servico/api_gateway.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Duas instâncias do Serviço A
INSTANCIAS_SERVICO_A = [
    "http://localhost:3001",
    "http://localhost:3003"   # segunda instância
]

SERVICO_B_URL = "http://localhost:3002"

# Contador para round-robin
contador_a = [0]

def proxima_instancia_a():
    instancia = INSTANCIAS_SERVICO_A[contador_a[0] % len(INSTANCIAS_SERVICO_A)]
    contador_a[0] += 1
    print(f"[API Gateway] Serviço A -> {instancia}")
    return instancia

@app.route('/itens', methods=['GET', 'POST'])
def tratar_itens():
    url = f"{proxima_instancia_a()}/itens"
    
    if request.method == 'GET':
        resp = requests.get(url)
    elif request.method == 'POST':
        resp = requests.post(url, json=request.get_json())
    
    return jsonify(resp.json()), resp.status_code

@app.route('/pedidos', methods=['GET', 'POST'])
def tratar_pedidos():
    if request.method == 'GET':
        resp = requests.get(f'{SERVICO_B_URL}/pedidos')
    elif request.method == 'POST':
        resp = requests.post(f'{SERVICO_B_URL}/pedidos', json=request.get_json())
    
    return jsonify(resp.json()), resp.status_code

if __name__ == "__main__":
    print("[API Gateway] A correr na porta 5000")
    app.run(port=5000)