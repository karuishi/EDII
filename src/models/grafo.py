import heapq

class GrafoRotas:
    def __init__(self):
        # Dicionário de adjacência (Rotas):
        # Ex: { 'Salvador': [ ('São Paulo', 'ED-001', 1200.0), ... ] }
        self.conexoes = {}
    
    def adicionar_rota(self, origem, destino, codigo_voo, preco):
        # Cria uma conexão entre dois aeroportos no grafo.
        if origem not in self.conexoes:
            self.conexoes[origem] = []
        if destino not in self.conexoes:
            self.conexoes[destino] = []

        # Adiciona o voo na lista de saídas da cidade de origem
        self.conexoes[origem].append((destino, codigo_voo, preco))
    
    def buscar_melhor_rota(self, aeroporto_partida, aeroporto_chegada):
        # Usa o algoritmo Dijkstra para encontrar a rota mais barata.
        # Retorna: (custo_total, [lista_de_voos] ou None)

        # Fila de prioridade: (custo_acumulado, cidade_atual, lista_de_voos)
        # O heapq sempre coloca o menor custo no topo da fila
        fila_prioridade = [(0, aeroporto_partida, [])]

        menores_custos = {aeroporto_partida: 0}

        visitados = set()

        while fila_prioridade:
            # Pega o caminho mais barato da fila
            custo_atual, cidade_atual, itinerario = heapq.heappop(fila_prioridade)

            # Se chegamos ao destino, retornamos o resultado
            if cidade_atual == aeroporto_chegada:
                return (custo_atual, itinerario)
            
            if cidade_atual in visitados:
                continue
            visitados.add(cidade_atual)

            # Explora as conexões (vizinhos)
            if cidade_atual in self.conexoes:
                for proximo_destino, codigo_voo, valor_passagem in self.conexoes[cidade_atual]:
                    novo_custo_total = custo_atual + valor_passagem

                    # Se encontramos um jeito mais barato
                    if proximo_destino not in menores_custos or novo_custo_total < menores_custos[proximo_destino]:
                        menores_custos[proximo_destino] = novo_custo_total
                        # Adiciona na fila para explorar depois
                        heapq.heappush(fila_prioridade, (novo_custo_total, proximo_destino, itinerario + [codigo_voo]))
                    
        return None
