from flask import Flask, request, jsonify

app = Flask(__name__)
pedidos = []

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    return jsonify(pedidos)

@app.route('/pedidos', methods=['POST'])
def add_pedido():
    data = request.get_json()  # get_json(), não get_jsonify()

    if not data or 'item_id' not in data or 'quantidade' not in data:
        return jsonify({'erro': 'É obrigatório preencher item_id e quantidade.'}), 400

    novo_pedido = {
        'id_pedido': len(pedidos) + 1,  # len(pedidos) + 1
        'id_item': data['item_id'],
        'quantidade': data['quantidade']
    }
    pedidos.append(novo_pedido)
    return jsonify(novo_pedido), 201

if __name__ == '__main__':
    app.run(port=3002)