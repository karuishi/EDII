def insertionSort(data):
    n = len(data)

    # O laço externo inicia no segundo elemento (posição 1)
    for i in range(1, n):
        # Este é o elemento que desejamo inserir na parte ordenada 
        item_chave = data[i]
        # j irá apontar para o último elemento na parte ordenada
        j = i - 1
        
        # Troca os elementos maiores que a chave uma posição para a direita
        while j >= 0 and item_chave['Chave'] < data[j]['Chave']:
            data[j + 1] = data[j]
            j -= 1

        data[j + 1] = item_chave
    
def printArray(arr):
    chaves = [item['Chave'] for item in arr]
    print(' '.join(map(str, chaves)))

if __name__ == "__main__":
    print("--- Teste com Caracteres (Exemplo 'ORDENA') ---")
    # Criando a lista de dicionários a partir da string "ORDENA"
    vetor_de_chars = [{'Chave': char} for char in "ORDENA"]

    print("Vetor original: ", end="")
    printArray(vetor_de_chars)

    insertionSort(vetor_de_chars)

    print("Vetor ordenado: ", end="")
    printArray(vetor_de_chars)
    print() # Adiciona uma linha em branco para separar os testes