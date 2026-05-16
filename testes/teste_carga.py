# testes/teste_carga.py
import threading
import requests
import time

URL_MONOLITO    = "http://localhost:8000"   # load balancer do monólito
URL_MICROSERVICO = "http://localhost:5000"  # api gateway

resultados = []
lock = threading.Lock()

def fazer_pedido(url, numero_utilizador):
    try:
        inicio = time.time()
        resp = requests.post(f"{url}/itens", json={"nome": f"Item_{numero_utilizador}"}, timeout=5)
        fim = time.time()
        
        duracao = round((fim - inicio) * 1000, 2)  # em milissegundos
        
        with lock:
            resultados.append({
                "utilizador": numero_utilizador,
                "status": resp.status_code,
                "tempo_ms": duracao,
                "sucesso": resp.status_code == 201
            })
    except Exception as e:
        with lock:
            resultados.append({
                "utilizador": numero_utilizador,
                "status": "ERRO",
                "tempo_ms": None,
                "sucesso": False
            })

def simular_carga(url, nome_sistema, num_utilizadores=50):
    print(f"\n{'='*50}")
    print(f"A testar: {nome_sistema} com {num_utilizadores} utilizadores")
    print(f"{'='*50}")
    
    resultados.clear()
    threads = []
    
    inicio_total = time.time()
    
    for i in range(num_utilizadores):
        t = threading.Thread(target=fazer_pedido, args=(url, i+1))
        threads.append(t)
    
    # Lançar todas as threads ao mesmo tempo
    for t in threads:
        t.start()
    
    # Esperar que todas terminem
    for t in threads:
        t.join()
    
    fim_total = time.time()
    
    # Calcular resultados
    sucessos = [r for r in resultados if r["sucesso"]]
    erros = [r for r in resultados if not r["sucesso"]]
    tempos = [r["tempo_ms"] for r in resultados if r["tempo_ms"] is not None]
    
    print(f"\nResultados para {nome_sistema}:")
    print(f"  Total de pedidos:   {num_utilizadores}")
    print(f"  Sucessos:           {len(sucessos)}")
    print(f"  Erros:              {len(erros)}")
    print(f"  Tempo total:        {round(fim_total - inicio_total, 2)}s")
    if tempos:
        print(f"  Tempo médio:        {round(sum(tempos)/len(tempos), 2)}ms")
        print(f"  Tempo mínimo:       {round(min(tempos), 2)}ms")
        print(f"  Tempo máximo:       {round(max(tempos), 2)}ms")

if __name__ == "__main__":
    simular_carga(URL_MONOLITO,     "Monólito com Load Balancer", num_utilizadores=50)
    simular_carga(URL_MICROSERVICO, "Microserviços com Gateway",  num_utilizadores=50)