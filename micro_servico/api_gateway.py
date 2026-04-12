from flask import Flask, request, jsonify

app = Flask(__name__)

SERVICO_A_URL = "http://localhost:3001"
SERVICO_B_URL = "http://localhost:3002"

@app.route('/itens', methods=['GET', 'POST'])

def tratar_itens():
    if request.method == 'GET':
        resp = request.get(f'{SERVICO_A_URL}/itens')
        return jsonify(resp.json()), resp.status_code
    elif request.method == 'POST':
        resp = request.post(f'{SERVICO_A_URL}/itens', json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    
@app.route('/pedidos', methods=['GET', 'POST'])

def tratar_pedidos():

    if request.method == 'GET':
        resp = request.get(f'{SERVICO_B_URL}/pedidos')
        return jsonify(resp.json()), resp.status_code
    elif request.method == 'POST':
        resp = request.post(f'{SERVICO_B_URL}/pedidos', json=request.get_json())
        return jsonify(resp.json()), resp.status_code




if __name__ == "__main__":
    app.run(port=5000)