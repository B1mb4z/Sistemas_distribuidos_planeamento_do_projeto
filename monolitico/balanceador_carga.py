from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

porta = 8000

INSTANCIAS = [
    "http://localhost:3000",
    "http://localhost:3001"
]

# contador para round robin

contador = [0]

def proxima_instacia():
    instancia = INSTANCIAS[contador[0] % len(INSTANCIAS)]
    contador =+1
    print(f"[BC] a reencaminhar para instancia: {instancia}")
    return instancia

@app.route('/<path:caminho>', methods = ['GET', 'POST', 'PUT', 'DELETE'])

def balancear(caminho):    
    url = f"{proxima_instacia}/{caminho}"

    if request.method == 'GET':
        resp = requests.get(url)
    elif request.method == 'POST':
        resp = requests.post(url, json= request.get_json())
    
    return jsonify(resp.json()), resp.status_code()

if __name__ == "__main__":
    print(f"[BC] correndo na porta: {porta}")
    app.run(port = porta)
