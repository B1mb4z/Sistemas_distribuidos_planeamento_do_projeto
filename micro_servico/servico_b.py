# micro_servico/servico_b.py
from flask import Flask, request, jsonify

app = Flask(__name__)
pedidos = []

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    print("[Serviço B] GET /pedidos")
    return jsonify(pedidos)

@app.route('/pedidos', methods=['POST'])
def add_pedido():
    data = request.get_json()

    if not data or 'item_id' not in data or 'quantidade' not in data:
        return jsonify({'erro': 'É necessário colocar item_id e quantidade.'}), 400

    novo_pedido = {
        "id_pedido": len(pedidos) + 1,
        'item_id': data['item_id'],
        'quantidade': data['quantidade']
    }
    pedidos.append(novo_pedido)
    print(f"[Serviço B] Pedido criado: {novo_pedido}")
    return jsonify(novo_pedido), 201

if __name__ == '__main__':
    print("[Serviço B] A correr na porta 3002")
    app.run(port=3002, threaded=True)