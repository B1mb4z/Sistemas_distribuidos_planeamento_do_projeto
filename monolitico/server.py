from flask import Flask, request, jsonify

app = Flask(__name__)

itens = []
pedidos = []

@app.route("/itens", methods=["GET"])
def get_items():
    return jsonify(itens)  # GET só lista, não cria

@app.route("/itens", methods=["POST"])
def add_item():
    data = request.get_json()  # get_json(), não get_data()

    if not data or "nome" not in data:
        return jsonify({"erro": "O nome é obrigatório."}), 400

    novo_item = {"id": len(itens) + 1, "nome": data["nome"]}  # len(itens) + 1
    itens.append(novo_item)
    return jsonify(novo_item), 201

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    return jsonify(pedidos)

@app.route('/pedidos', methods=['POST'])
def add_pedido():
    data = request.get_json()  # get_json(), não get_jsonify()

    if not data or 'item_id' not in data or 'quantidade' not in data:
        return jsonify({'erro': 'É necessário colocar item_id e quantidade.'}), 400

    novo_pedido = {
        "id_pedido": len(pedidos) + 1,  # len(pedidos) + 1
        'item_id': data['item_id'],
        'quantidade': data['quantidade']
    }
    pedidos.append(novo_pedido)
    return jsonify(novo_pedido), 201

if __name__ == "__main__":
    app.run(port=3000, debug=True)