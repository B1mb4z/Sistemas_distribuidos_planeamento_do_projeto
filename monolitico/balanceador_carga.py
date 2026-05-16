from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCIAS = [
    "http://localhost:3000",
    "http://localhost:3001"
]

contador = [0]

def proxima_instancia():
    global contador
    instancia = INSTANCIAS[contador[0] % len(INSTANCIAS)]
    contador[0] += 1
    print(f"[Load Balancer] A reencaminhar para: {instancia}")
    return instancia

@app.route('/<path:caminho>', methods=['GET', 'POST'])
def balancear(caminho):
    url = f"{proxima_instancia()}/{caminho}"

    try:
        if request.method == 'GET':
            resp = requests.get(url, timeout=5)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.get_json(), timeout=5)

        # Verifica se a resposta tem conteúdo antes de fazer .json()
        if resp.content:
            return jsonify(resp.json()), resp.status_code
        else:
            return jsonify({"erro": "Resposta vazia do servidor"}), 502

    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Servidor indisponível"}), 503
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    print("[Load Balancer Monolito] A correr na porta 8000")
    app.run(port=8000, threaded=True)  # threaded=True para aceitar pedidos em paralelofrom flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCIAS = [
    "http://localhost:3000",
    "http://localhost:3001"
]

contador = [0]

def proxima_instancia():
    global contador
    instancia = INSTANCIAS[contador[0] % len(INSTANCIAS)]
    contador[0] += 1
    print(f"[Load Balancer] A reencaminhar para: {instancia}")
    return instancia

@app.route('/<path:caminho>', methods=['GET', 'POST'])
def balancear(caminho):
    url = f"{proxima_instancia()}/{caminho}"

    try:
        if request.method == 'GET':
            resp = requests.get(url, timeout=5)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.get_json(), timeout=5)

        # Verifica se a resposta tem conteúdo antes de fazer .json()
        if resp.content:
            return jsonify(resp.json()), resp.status_code
        else:
            return jsonify({"erro": "Resposta vazia do servidor"}), 502

    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Servidor indisponível"}), 503
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    print("[Load Balancer Monolito] A correr na porta 8000")
    app.run(port=8000, threaded=True)  # threaded=True para aceitar pedidos em paralelo