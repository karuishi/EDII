import heapq

class GrafoRotas:
    def __init__(self):
        # O Grafo é basicamente um dicionário. A chave é a cidade, e os valores são as rotas saindo dela
        # Exemplo: { 'Salvador': [ ('São Paulo', 'ED-001', 1200.0), ... ] }
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
        # O Dijkstra é utilizado para achar a sequência de voos mais barata entre duas cidades.
        # Ele retorna o custo total e a lista de voos que o passageiro tem que pegar

        # A Fila de prioridade funciona como: (custo_acumulado, cidade_atual, lista_de_voos)
        # O heap sempre encontra o menor custo e o coloca no topo da fila
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

                    # Se achamos um caminho mais barato pra essa cidade
                    if proximo_destino not in menores_custos or novo_custo_total < menores_custos[proximo_destino]:
                        menores_custos[proximo_destino] = novo_custo_total
                        # Adiciona na fila para continuar explorando a partir daqui
                        heapq.heappush(fila_prioridade, (novo_custo_total, proximo_destino, itinerario + [codigo_voo]))
                    
        return None
