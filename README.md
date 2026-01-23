✈️ SOL Airlines - Sistema de Gestão de Voos

Sistema de gerenciamento de passagens aéreas desenvolvido em Python com Flask. O projeto se destaca pela implementação manual de estruturas de dados complexas para otimização de buscas e rotas.

🧠 Diferenciais Técnicos

Este não é apenas um CRUD simples. O núcleo do sistema utiliza algoritmos avançados:

    Árvore B (B-Tree): Implementada do zero (src/BTree.py) para indexação e busca otimizada de clientes por CPF, garantindo alta performance mesmo com grandes volumes de dados.

    Teoria dos Grafos & Dijkstra: O sistema de rotas (src/grafo.py) utiliza um grafo ponderado onde os aeroportos são vértices e os voos são arestas. O algoritmo de Dijkstra é usado para encontrar automaticamente a rota mais barata entre dois destinos (incluindo conexões).

🚀 Tecnologias

    Backend: Python 3, Flask (Blueprints, Session management)

    Frontend: HTML5, Bootstrap 5, Jinja2

    Mapas: Integração com Folium para visualização de rotas

    Dados: Persistência em JSON (Simulação de NoSQL)

🛠️ Como executar

    Clone o repositório:
    Bash

    git clone https://github.com/karuishi/EDII.git

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Execute a aplicação:
    Bash

    python app.py

    Acesse no navegador: http://127.0.0.1:5000