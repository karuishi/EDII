def heapify(data, n, i):
    """
    Função para transformar um subtree em um max-heap.
    'data' é a lista, 'n' é o tamanho do heap, 'i' é o índice da raiz do subtree.
    """
    maior = i       # Inicializa o maior como a raiz
    esq = 2 * i + 1 # Filho da esquerda (fórmula para base 0)
    dir = 2 * i + 2 # Filho da direita (fórmula para base 0)

    # Verifica se o filho da esquerda existe e é maior que a raiz
    if esq < n and data[esq]['chave'] > data[maior]['chave']:
        maior = esq

    # Verifica se o filho da direita existe e é maior que o "maior" até agora
    if dir < n and data[dir]['chave'] > data[maior]['chave']:
        maior = dir

    # Se o maior não for mais a raiz, troca e continua o heapify
    if maior != i:
        data[i], data[maior] = data[maior], data[i]  # Swap
        heapify(data, n, maior)

def heap_sort(data):
    """
    Função principal que aplica o HeapSort em uma lista de dicionários.
    """
    n = len(data)

    # 1. Constrói um max-heap a partir da lista desordenada.
    # Começa do último nó não-folha e vai até a raiz.
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    # 2. Extrai os elementos um por um do heap.
    for i in range(n - 1, 0, -1):
        # Move a raiz atual (o maior elemento) para o fim da lista
        data[i], data[0] = data[0], data[i]  # Swap
        
        # Chama o heapify no heap reduzido para manter a propriedade de max-heap
        heapify(data, i, 0)

def print_array(arr):
    chaves = [item['chave'] for item in arr]
    print(' '.join(map(str, chaves)))

if __name__ == "__main__":
    # --- Teste com números inteiros ---
    print("--- Teste com Números Inteiros ---")
    
    # Criando a lista de dicionários a partir de uma lista de números
    vetor_de_ints = [{'chave': num} for num in [64, 25, 12, 22, 11, 90]]

    print("Vetor original:  ", end="")
    print_array(vetor_de_ints)
    
    heap_sort(vetor_de_ints)
    
    print("Vetor ordenado:  ", end="")
    print_array(vetor_de_ints)