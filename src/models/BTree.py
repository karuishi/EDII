class BTreeNode:
    # Representa uma Página (Nó) da Árvore B de Clientes.
    def __init__(self, eh_folha = False):
        # True se este não tiver filhos
        self.eh_folha = eh_folha
        
        # Lista ordenada dos CPFs armazenados 
        self.cpfs = []

        # Lista de referência para os nós filhos
        self.filhos = []

class BTree:
    def __init__(self, grau_min):
        # Cria a raiz inicial (vazia)
        self.raiz = BTreeNode(eh_folha=True)
        self.grau_min = grau_min

    def buscar(self, cpf_buscado):
        # Verifica se o CPF existe
        return self._buscar_na_pagina(self.raiz, cpf_buscado)
    
    def _buscar_na_pagina(self, pagina, cpf):
        # Busca interna recursiva para navegar nas páginas
        i = 0
        # 1. Procura o CPF dentro da página atual
        while i < len(pagina.cpfs) and cpf > pagina.cpfs[i]:
            i += 1
        
        # 2. Se achou o CPF exato
        if i < len(pagina.cpfs) and cpf == pagina.cpfs[i]:
            return True 
        
        # 3. Se chegou numa folha e não achou
        if pagina.eh_folha:
            return False
        
        # 4. Se não achou, desce para a página filha apropriada
        return self._buscar_na_pagina(pagina.filhos[i], cpf)
    
    def inserir(self, novo_cpf):
        # Adiciona um novo CPF ao índice.
        raiz_atual = self.raiz
        t = self.grau_min

        # Se a raiz estiver cheia, a árvore precisa crescer em altura
        if len(raiz_atual.cpfs) == (2 * t) - 1:
            nova_raiz = BTreeNode()
            self.raiz = nova_raiz

            # A antiga raiz vira filha da nova
            nova_raiz.filhos.insert(0, raiz_atual)

            # Divide a antiga raiz ao meio
            self._dividir_pagina(nova_raiz, 0)

            # Inserir o CPF na nova estrutura
            self._inserir_nao_cheio(nova_raiz, novo_cpf)
        else:
            self._inserir_nao_cheio(raiz_atual, novo_cpf)

    def _inserir_nao_cheio(self, pagina, cpf):
        # Insere o CPF em uma página que tem espaço

        i = len(pagina.cpfs) - 1

        if pagina.eh_folha:
            # Se for folha, insere direto na posição correta
            pagina.cpfs.append(0)
            while i >= 0 and cpf < pagina.cpfs[i]:
                pagina.cpfs[i + 1] = pagina.cpfs[i]
                i -= 1
            pagina.cpfs[i + 1] = cpf
        else:
            # Se não for folha, descobre para qual filho descer
            while i >= 0 and cpf < pagina.cpfs[i]:
                i -= 1
            i += 1

            # verifica se o filtro está cheio antes de entrar
            if len(pagina.filhos[i].cpfs) == (2 * self.grau_min) - 1:
                self._dividir_pagina(pagina, i)
                if cpf > pagina.cpfs[i]:
                    i += 1
            self._inserir_nao_cheio(pagina.filhos[i], cpf)
    
    def _dividir_pagina(self, pagina_pai, indice_filho):
        # Divide uma página cheia em duas e sobe o elemento mediano

        t = self.grau_min
        pagina_cheia = pagina_pai.filhos[indice_filho]
        nova_pagina_irma = BTreeNode(eh_folha=pagina_cheia.eh_folha)

        # O CPF do meio sobre para o pai
        cpf_mediano = pagina_cheia.cpfs[t - 1]
        pagina_pai.cpfs.insert(indice_filho, cpf_mediano)

        # Conecta a nova irmã ao pai
        pagina_pai.filhos.insert(indice_filho + 1, nova_pagina_irma)

        # Move a metade direita dos CPFs para a nova página
        nova_pagina_irma.cpfs = pagina_cheia.cpfs[t:]
        pagina_cheia.cpfs = pagina_cheia.cpfs[:t - 1]

        # Se tiver filhos, move eles também
        if not pagina_cheia.eh_folha:
            nova_pagina_irma.filhos = pagina_cheia.filhos[t:]
            pagina_cheia.filhos = pagina_cheia.filhos[:t]
    
    def listar_cpfs(self):
        # Retorna todos os CPFs em ordem crescente.
        lista_resultado = []
        self._percorrer_em_ordem(self.raiz, lista_resultado)
        return lista_resultado
    
    def _percorrer_em_ordem(self, pagina, lista):
        for i in range(len(pagina.cpfs)):
            if not pagina.eh_folha:
                self._percorrer_em_ordem(pagina.filhos[i], lista)
            lista.append(pagina.cpfs[i])
        
        if not pagina.eh_folha:
            self._percorrer_em_ordem(pagina.filhos[len(pagina.cpfs)], lista)