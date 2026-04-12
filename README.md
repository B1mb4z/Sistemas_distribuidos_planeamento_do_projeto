
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
