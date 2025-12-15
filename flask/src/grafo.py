import heapq

class Graph:
    def __init__(self):
        # Dicionário de adjacência:
        # { 'Origem': [ ('Destino', 'CodigoVoo', Preco), ... ] }
        self.adj = {}

    def add_edge(self, u, v, codigo, preco):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        
        # Adiciona a aresta (voo)
        self.adj[u].append((v, codigo, preco))

    def dijkstra(self, start, end):
        """
        Encontra o caminho mais barato entre 'start' e 'end'.
        Retorna: (custo_total, [lista_de_codigos_dos_voos]) ou None
        """
        # Fila de prioridade: (custo_acumulado, cidade_atual, caminho_voos)
        pq = [(0, start, [])]
        
        # Para rastrear o menor custo encontrado até cada cidade
        min_costs = {start: 0}
        
        visited = set()

        while pq:
            cost, u, path = heapq.heappop(pq)

            # Se chegamos ao destino, retornamos o resultado
            if u == end:
                return (cost, path)

            if u in visited:
                continue
            visited.add(u)

            # Explora os vizinhos (voos saindo de u)
            if u in self.adj:
                for v, codigo, preco in self.adj[u]:
                    new_cost = cost + preco
                    
                    # Se encontramos um caminho mais barato para 'v', atualizamos
                    if v not in min_costs or new_cost < min_costs[v]:
                        min_costs[v] = new_cost
                        heapq.heappush(pq, (new_cost, v, path + [codigo]))
        
        return None