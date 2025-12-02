class BTreeNode:
    """
    Representa um Nó (ou Página) numa Árvore B.
    """
    def __init__(self, leaf=False):
        # 'leaf' (folha) é True se este nó está na base da árvore (não tem filhos)
        self.leaf = leaf
        
        # 'keys' é a lista de chaves (os nossos CPFs) que este nó armazena.
        # Esta lista estará sempre ordenada.
        self.keys = []
        
        # 'children' é a lista de nós filhos (outras "gavetas" para onde este nó aponta)
        self.children = []

class BTree:
    """
    A implementação completa da Árvore B.
    't' é o "grau mínimo" da árvore. É a regra mais importante.
    Uma escolha comum é t=3, o que significa que cada nó deve ter:
    - No mínimo (t-1) = 2 chaves
    - No máximo (2t-1) = 5 chaves
    Isto garante que a árvore se mantenha "balanceada" e rápida.
    """
    def __init__(self, t):
        # A raiz da árvore começa como um nó folha vazio
        self.root = BTreeNode(leaf=True)
        # 't' é o grau mínimo
        self.t = t

    # ----------------------------------------------
    # FUNÇÃO 1: PROCURAR (SEARCH)
    # ----------------------------------------------
    def search(self, key_to_find):
        """
        Procura por uma 'key_to_find' (um CPF) na árvore.
        Retorna True se encontrar, False se não.
        """
        return self._search_in_node(self.root, key_to_find)

    def _search_in_node(self, node, key_to_find):
        """
        Função auxiliar recursiva para procurar no nó 'node'.
        """
        i = 0
        # 1. Encontra a primeira chave no nó que é >= 'key_to_find'
        while i < len(node.keys) and key_to_find > node.keys[i]:
            i += 1

        # 2. Verifica se encontrámos a chave
        if i < len(node.keys) and key_to_find == node.keys[i]:
            return True  # Encontrado!

        # 3. Se este nó é uma folha, não temos para onde ir
        if node.leaf:
            return False # Não encontrado

        # 4. Se não é uma folha, desce para o filho apropriado
        #    (o filho à esquerda da chave que encontrámos)
        return self._search_in_node(node.children[i], key_to_find)

    # ----------------------------------------------
    # FUNÇÃO 2: INSERIR (INSERT) - A PARTE MAIS COMPLEXA
    # ----------------------------------------------
    def insert(self, key_to_insert):
        """
        Função principal para inserir uma nova 'key_to_insert' (um CPF).
        """
        t = self.t
        root = self.root

        # Caso 1: A Raiz está "cheia" (atingiu o n.º máximo de chaves)
        # Se a raiz está cheia, a árvore tem de crescer em altura.
        if len(root.keys) == (2 * t) - 1:
            # Cria uma nova raiz
            new_root = BTreeNode()
            self.root = new_root
            
            # A antiga raiz torna-se o primeiro filho da nova raiz
            new_root.children.insert(0, root)
            
            # "Divide" a antiga raiz (que estava cheia)
            self._split_child(new_root, 0)
            
            # Agora que a raiz tem espaço, insere a chave
            self._insert_non_full(new_root, key_to_insert)
        
        # Caso 2: A Raiz não está cheia
        # Simplesmente chama a função para inserir no nó
        else:
            self._insert_non_full(root, key_to_insert)

    def _insert_non_full(self, node, key_to_insert):
        """
        Função auxiliar para inserir uma chave num nó que *não* está cheio.
        """
        t = self.t
        i = len(node.keys) - 1

        # A. Se o nó é uma folha (base da árvore)
        if node.leaf:
            # Adiciona um espaço temporário
            node.keys.append(0) 
            # Move todas as chaves maiores para a direita
            while i >= 0 and key_to_insert < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            # Insere a chave na posição correta
            node.keys[i + 1] = key_to_insert
        
        # B. Se o nó não é uma folha (é um nó interno)
        else:
            # Encontra o filho para onde temos de descer
            while i >= 0 and key_to_insert < node.keys[i]:
                i -= 1
            i += 1 # O índice do filho correto

            # B.1. Verifica se o filho para onde vamos descer está cheio
            if len(node.children[i].keys) == (2 * t) - 1:
                # Se o filho está cheio, "divide-o" ANTES de descer
                self._split_child(node, i)
                # Vê para qual dos dois novos filhos devemos descer
                if key_to_insert > node.keys[i]:
                    i += 1
            
            # B.2. Desce recursivamente para o filho (que agora sabemos que não está cheio)
            self._insert_non_full(node.children[i], key_to_insert)

    def _split_child(self, parent_node, child_index):
        """
        Função para "dividir" um nó filho que está cheio.
        'parent_node' é o nó pai.
        'child_index' é o índice do filho que está cheio.
        """
        t = self.t
        
        # O nó filho que está cheio
        child_node = parent_node.children[child_index]
        
        # O novo nó que será o "irmão" direito do 'child_node'
        new_sibling = BTreeNode(leaf=child_node.leaf)

        # A chave do "meio" do nó filho sobe para o nó pai
        middle_key = child_node.keys[t - 1]
        parent_node.keys.insert(child_index, middle_key)
        
        # O novo nó "irmão" é adicionado como filho do pai
        parent_node.children.insert(child_index + 1, new_sibling)

        # Copia a segunda metade das chaves do nó filho para o novo nó "irmão"
        new_sibling.keys = child_node.keys[t:]
        
        # Apaga a segunda metade das chaves do nó filho (que agora estão no "irmão")
        child_node.keys = child_node.keys[:t - 1]

        # Se o nó filho não era uma folha, copia também os filhos
        if not child_node.leaf:
            new_sibling.children = child_node.children[t:]
            child_node.children = child_node.children[:t]

    # ----------------------------------------------
    # FUNÇÃO 3: PERCORRER - PARA ORDENAÇÃO
    # ----------------------------------------------
    def in_order_list(self):
        """
        Retorna uma lista com todos os CPFs ordenados, percorrendo a árvore.
        """
        result = []
        self._in_order_list_node(self.root, result)
        return result
    
    def _in_order_list_node(self, node, result):
        """
        Função auxiliar recursiva para preencher a lista.
        """
        for i in range(len(node.keys)):
            # 1. Visita o filho à esquerda da chave atual (se existir)
            if not node.leaf:
                self._in_order_list_node(node.children[i], result)
            # 2. Adiciona a chave (CPF) à nossa lista de resultados
            result.append(node.keys[i])
        # 3. Visita o último filho (à direita da última chave)
        if not node.leaf:
            self._in_order_list_node(node.children[len(node.keys)], result)