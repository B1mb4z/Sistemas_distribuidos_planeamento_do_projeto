from flask import Flask, request, jsonify

app = Flask(__name__)
itens = []

@app.route('/itens', methods=['GET'])
def get_itens():
    return jsonify(itens)

@app.route('/itens', methods=['POST'])
def add_itens():
    data = request.get_json()  # get_json(), não get_jsonify()

    if not data or 'nome' not in data:  # 'not in', não 'in'
        return jsonify({'erro': 'É obrigatório preencher o campo nome.'}), 400

    novo_item = {
        'id': len(itens) + 1,  # len(itens) + 1
        'nome': data['nome'],
        'preco': data.get('preco', 0)  # .get() para não crashar se preco vier vazio
    }
    itens.append(novo_item)
    return jsonify(novo_item), 201

if __name__ == '__main__':
    app.run(port=3001)