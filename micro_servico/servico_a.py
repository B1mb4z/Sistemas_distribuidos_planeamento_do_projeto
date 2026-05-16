# micro_servico/servico_a.py
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
itens = []

PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 3001

@app.route('/itens', methods=['GET'])
def get_itens():
    print(f"[Servico A - porta {PORTA}] GET /itens")
    return jsonify(itens)

@app.route('/itens', methods=['POST'])
def add_itens():
    data = request.get_json()

    if not data or 'nome' not in data:
        return jsonify({'erro': 'É obrigatório preencher o campo nome.'}), 400

    novo_item = {
        'id': len(itens) + 1,
        'nome': data['nome'],
        'preco': data.get('preco', 0),
        'respondido_por': f"Servico A porta {PORTA}"  # para ver qual instância respondeu
    }
    itens.append(novo_item)
    print(f"[Servico A - porta {PORTA}] Item criado: {novo_item['nome']}")
    return jsonify(novo_item), 201

if __name__ == '__main__':
    print(f"[Servico A] A correr na porta {PORTA}")
    app.run(port=PORTA)