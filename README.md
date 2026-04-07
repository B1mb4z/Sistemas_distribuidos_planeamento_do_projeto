Com base no PDF que você forneceu, estruturei o **README.md** e o restante da documentação teórica necessária para o trabalho.

Abaixo está o conteúdo organizado. Como solicitado, utilizei o tema **Restaurante** para a implementação prática. Este material cobre a pesquisa teórica, as instruções de configuração e a documentação das arquiteturas.

---

# Trabalho: Centralizado vs Distribuído (API Gateway Simples)
**Tema:** Sistema de Cardápio e Pedidos para Restaurante

## Pesquisa e Fundamentação Teórica

### Arquitetura Monolítica
A arquitetura monolítica é o modelo tradicional de desenvolvimento de software onde toda a aplicação (Interface de Usuário, Regras de Negócio, Acesso a Dados) é construída como uma única unidade .
- **Características:** Código-fonte único, base de dados centralizada, deploy único.
- **Vantagens:** Simplicidade no desenvolvimento inicial, fácil depuração, menor latência interna (chamadas de função vs rede).
- **Desvantagens:** Dificuldade para escalar (é preciso replicar o app inteiro), alta complexidade com o tempo (acoplamento), qualquer mudança exige rebuild total.

### Arquitetura Distribuída (Microservices)
A arquitetura de microserviços estrutura a aplicação como um conjunto de serviços pequenos, independentes e focados em uma única funcionalidade .
- **Características:** Serviços desacoplados, deploy independente, tecnologias podem variar entre serviços.
- **Vantagens:** Escalabilidade horizontal seletiva (escala só o que precisa), resiliência (falha em um não derruba tudo), facilidade para atualizações.
- **Desvantagens:** Complexidade operacional (orquestração), latência de rede, consistência eventual de dados.

### O Papel do API Gateway
O API Gateway atua como o "ponto único de entrada" para os clientes .
- **Em Monolitos:** Funciona principalmente como um *Reverse Proxy* ou Load Balancer, direcionando tráfego para a aplicação principal .
- **Em Microservices:** Tem papel ativo: roteamento inteligente, agregação de dados (compor resposta de vários serviços), autenticação (JWT) e observabilidade .

---

##  Arquitetura Proposta (Tema: Restaurante)

Para a demonstração, implementaremos um sistema simples de **Cardápio e Pedidos**.

### Arquitetura Monolítica (Centralizada)
- **Estrutura:** Uma única aplicação (Node.js + Express) que contém:
    - Módulo `Menu`: Listar pratos.
    - Módulo `Orders`: Criar pedidos.
    - Banco de dados SQLite (único).
- **Gateway:** Nginx agindo como proxy reverso simples.

### Arquitetura Distribuída (Microservices + Gateway)
- **Estrutura:**
    - **API Gateway (Porta 8080):** Ponto de entrada. Roteia requisições, valida JWT.
    - **Auth Service (Porta 8081):** Responsável por login/registro e emissão de tokens.
    - **Menu Service (Porta 8082):** Gerencia os itens do cardápio.
    - **Order Service (Porta 8083):** Gerencia os pedidos e se comunica com o Menu para validar itens .
- **Comunicação:** HTTP/REST (para simplicidade) entre os serviços internos.

---




## Comparação de Resultados

| Característica | Monolito | Microservices + Gateway |
| :--- | :--- | :--- |
| **Complexidade Inicial** | Baixa | Alta (gerenciar 4 servidores) |
| **Performance (Latência)** | Baixa (chamada local) | Média (overhead de rede + HTTP) |
| **Escalabilidade** | Escala a aplicação inteira | Escala **apenas** o serviço sobrecarregado (ex: Orders) |
| **Resiliência** | Baixa (um erro derruba tudo) | Média (Gateway pode isolar serviço falho) |
| **Segurança Centralizada** | Feita dentro da app | **Gateway** unifica a validação JWT  |

## Decisões Técnicas & Justificativas

- **Node.js + Express:** Escolhido pela leveza e facilidade para simular serviços HTTP de forma rápida, focando no conceito de arquitetura em vez da sintaxe da linguagem.
- **JWT (JSON Web Token):** Utilizado no modelo distribuído para stateless authentication. O API Gateway valida o token, e o header é repassado aos serviços internos .
- **Banco de Dados:** Optou-se por SQLite (monolito) e "in-memory" (microservices) para evitar dependências externas (Docker) no setup, garantindo que o avaliador consiga rodar o código instantaneamente.
- **Proxy Reverso (Nginx vs Código):** No monolito, o Nginx age como um simples redirecionador. Nos microservices, o Gateway (código puro) age como um **orquestrador**, agregando dados quando necessário.


## Scripts de Código (Exemplo Base)

**`microservices/api-gateway/server.js`**
```javascript
const express = require('express');
const axios = require('axios'); // Para chamar os outros serviços
const app = express();

const AUTH_URL = 'http://localhost:8081';
const MENU_URL = 'http://localhost:8082';

// Middleware para verificar JWT
const verifyToken = async (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) return res.status(401).json({ error: 'Token required' });

    const token = authHeader.split(' ')[1];
    try {
        // Pergunta ao Auth Service se o token é válido
        const response = await axios.get(`${AUTH_URL}/verify`, { headers: { Authorization: `Bearer ${token}` } });
        req.user = response.data; // Salva info do usuário
        next();
    } catch (error) {
        res.status(403).json({ error: 'Invalid token' });
    }
};

// Rota pública: Login (Gateway apenas redireciona)
app.post('/auth/login', async (req, res) => {
    const response = await axios.post(`${AUTH_URL}/login`, req.body);
    res.json(response.data);
});

// Rota privada: Cardápio (Gateway valida token e roteia)
app.get('/menu', verifyToken, async (req, res) => {
    const response = await axios.get(`${MENU_URL}/items`);
    res.json(response.data);
});

app.listen(8080, () => console.log('Gateway running on port 8080'));
```

