from flask import Flask, request, jsonify

app = Flask(__name__)

itens = []

@app.route('/itens')

def get_itens():
    return jsonify(itens)

@app.route('/itens', methods=['POST'])

def add_itens():
    data = request.get_jsonify()

    if not data or 'nome' in data:
        return jsonify({'erro': 'É obrigatório preencher o campo nome.'}), 400
    novo_item = {
        'id': len(itens + 1),
        'nome': data['nome'],
        'preco': data['preco']
    }
    itens.append(novo_item)
    return jsonify(novo_item), 201



if __name__ == '__main__':
    app.run(port= 3001)