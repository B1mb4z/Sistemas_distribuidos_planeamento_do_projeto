import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
itens = []
pedidos = []


@app.route("/itens", methods=["GET"])

def get_items():
    data = request.get_data()
    
    if not data or "nome" not in data:
        return jsonify({"erro":"O nome e obrigatorio."}), 400
    novo_item = {"id": len(itens + 1), "nome": data["nome"] }
    itens.append(novo_item)
    
    return jsonify(novo_item), 201

@app.route('/pedidos', methods=['GET'])
    
def get_pedidos():    
    return jsonify(pedidos)

@app.route('/pedidos', methods=['POST'])

def add_pedidos():
    data = request.get_jsonify()

    if not data or 'item_id' not in data or 'quantity' not in data:
        return jsonify({'erro': 'É necessario colocar id e quantidade.'}), 400
    
    novo_pedido = {
        "id_pedido": len(pedidos +1),
        'pedido': data['item_id'],
        'quanitade': data['quantity']
    }


    pedidos.append(novo_pedido)
    return jsonify(novo_pedido), 201





if __name__ == "__main__":
    porta = (sys.argv[1]) if len(sys.argv) > 1 else 3000
    print(f"[Monolitico] a correr na porta {porta}")
    app.run(port=porta, debug=True)
