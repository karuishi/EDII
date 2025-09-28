def particao(data, Esq, Dir):
    # Escolhe o pivô como o elemento do meio 
    pivo = data[(Esq + Dir) // 2]

    while Esq <= Dir:
        # Encontra um elemento à Esquerda que deveria estar à Dirita
        while pivo['chave'] > data[Esq]['chave']:
            Esq += 1

        # Encontra um elemento à Dirita que deveria estar à Esquerda
        while pivo['chave'] < data[Dir]['chave']:
            Dir -= 1
        
        # Se os ponteiros não se cruzaram, troca os elementos
        if Esq <= Dir:
            data[Esq], data[Dir] = data[Dir], data[Esq]

            # Move os ponteiros para evitar loop infinito caso os
            # elementos sejam iguais ao pivô. O código C original não tem isso.
            Esq += 1
            Dir -= 1
    
    return Esq, Dir

def quickSort(data, Esq, Dir):
    indice_meio_Esq, indice_meio_Dir = particao(data, Esq, Dir)

    if Esq < Dir:
        quickSort(data, Esq, indice_meio_Dir)
    
    if Dir > Esq:
        quickSort(data, Dir, indice_meio_Esq)

def print_array(arr):
    """Função auxiliar para imprimir as chaves do array."""
    chaves = [item['chave'] for item in arr]
    print(' '.join(map(str, chaves)))

# --- Exemplo de Uso ---
if __name__ == "__main__":
    print("--- Teste com QuickSort (Exemplo 'ORDENA') ---")
    
    vetor_de_chars = [{'chave': char} for char in "ORDENA"]

    print("Vetor original: ", end="")
    print_array(vetor_de_chars)

    # Inicia a chamada do QuickSort para o vetor completo
    quickSort(vetor_de_chars, 0, len(vetor_de_chars) - 1)

    print("Vetor ordenado (decrescente): ", end="")
    print_array(vetor_de_chars)