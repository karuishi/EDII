def selection_sort(data):
    n = len(data)

    # O laço externo percorre a lista do início ao penúltimo elemento.
    # Corresponde a: for(i=1; i<=*n-1; i++)
    for i in range(n - 1):
        min = i;
        # Corresponde a: for (j=i+1; j<=*n; j++)
        for j in range(i + 1, n):
            # Corresponde a: if (A[j].Chave < A[Min].Chave)
            if data[j]['Chave'] < data[min]['Chave']:
                min = j; # Atualiza o índice do menor elemento

        # Troca o menor elemento encontrado com o primeiro elemento da parte não ordenada
        if min != i:
            # Corresponde a: x = A[min]; A[min] = A[i]; A[i] = x;
            data[i], data[min] = data[min], data[i]

def printArray(arr):
    chaves = [item['Chave'] for item in arr]
    print(' '.join(map(str, chaves)))

if __name__ == "__main__":
    print("--- Teste com Caracteres (Exemplo 'ORDENA') ---")
    # Criando a lista de dicionários a partir da string "ORDENA"
    vetor_de_chars = [{'Chave': char} for char in "ORDENA"]

    print("Vetor original: ", end="")
    printArray(vetor_de_chars)

    selection_sort(vetor_de_chars)

    print("Vetor ordenado: ", end="")
    printArray(vetor_de_chars)
    print() # Adiciona uma linha em branco para separar os testes

    # --- Teste 2: Com números inteiros ---
    print("--- Teste com Números Inteiros ---")
    
    # Criando a lista de dicionários a partir de uma lista de números
    vetor_de_ints = [{'Chave': num} for num in [64, 25, 12, 22, 11, 90]]

    print("Vetor original: ", end="")
    printArray(vetor_de_ints)
    
    selection_sort(vetor_de_ints)
    
    print("Vetor ordenado: ", end="")
    printArray(vetor_de_ints)