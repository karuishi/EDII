# ✈️ SOL Airlines — Sistema de Gestão de Voos

Sistema de gerenciamento de passagens aéreas desenvolvido em **Python** com **Flask**. O projeto se destaca pela implementação manual de estruturas de dados complexas para otimização de buscas e rotas.

## 🧠 Diferenciais Técnicos

Este não é apenas um CRUD simples. O núcleo do sistema utiliza algoritmos avançados:

- **Árvore B (B-Tree):** Implementada do zero (`src/models/BTree.py`) para indexação e busca otimizada de clientes por CPF, garantindo alta performance mesmo com grandes volumes de dados.

- **Teoria dos Grafos & Dijkstra:** O sistema de rotas (`src/models/grafo.py`) utiliza um grafo ponderado onde os aeroportos são vértices e os voos são arestas. O algoritmo de Dijkstra é usado para encontrar automaticamente a rota mais barata entre dois destinos (incluindo conexões).

## 🚀 Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3, Flask (Blueprints, Session) |
| Frontend | HTML5, Bootstrap 5, Jinja2 |
| Mapas | Folium (visualização de rotas) |
| Dados | Persistência em JSON (Simulação NoSQL) |

## 📁 Estrutura do Projeto

```
EDII/
├── app.py                  # Ponto de entrada Flask
├── data/                   # Arquivos JSON (banco de dados)
│   ├── clientes.json
│   ├── login.json
│   ├── reservas.json
│   └── voos.json
├── src/
│   ├── database.py         # Carregamento global de dados
│   ├── models/
│   │   ├── BTree.py        # Implementação da Árvore B
│   │   ├── data_manager.py # CRUD de arquivos JSON
│   │   └── grafo.py        # Grafo + Dijkstra
│   └── routes/
│       ├── admin.py        # Rotas de administração
│       ├── auth.py         # Login / Logout / Criar conta
│       └── passageiro.py   # Dashboard do passageiro
├── static/
│   └── style.css           # Estilos globais
├── templates/              # Templates Jinja2
│   ├── tela_inicial/       # Home + Base layout
│   ├── login/              # Login + Criar conta
│   ├── passageiros/        # Dashboard + Cartão de embarque
│   ├── voos/               # CRUD de voos (admin)
│   ├── clientes/           # CRUD de clientes (admin)
│   └── reservas/           # CRUD de reservas (admin)
└── requirements.txt
```

## 🛠️ Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/karuishi/EDII.git
   cd EDII
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   python app.py
   ```

4. **Acesse no navegador:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 👥 Credenciais de Teste

| Usuário | Senha | Perfil |
|---------|-------|--------|
| `Admin` | `Farcry34!` | Administrador |
| `Sunoo` | `Sunghoonvida` | Cliente |