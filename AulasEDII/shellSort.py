def shellSort(data):
    n = len(data)

    gap = 1
    while gap < n // 3:
        gap = 3 * gap + 1

    # Começa com o maior gap e o reduz até h ser 1
    while gap > 0:
         # Este loop percorre os elementos que serão comparados.
        for i in range(gap, n): 
            # Guarda o elemento atual para inseri-lo na posição correta
            item_chave = data[i]
            j = i

            # Desloca os elementos anteriores (a uma distância 'gap') que são maiores
            # que o 'item_chave' para a direita
            while j >= gap and data[j - gap]['Chave'] > item_chave['Chave']:
                data[j] = data[j - gap]
                j -= gap
            
            # Insere o elemento guardado ('key_item') na sua posição correta
            data[j] = item_chave

        # Reduz o gap para a próxima iteração
        gap = gap // 3

def print_array(arr):
    """Função auxiliar para imprimir as chaves do array."""
    chaves = [item['Chave'] for item in arr]
    print(' '.join(map(str, chaves)))

# --- Exemplo de Uso ---
if __name__ == "__main__":
    print("--- Teste com Caracteres (Exemplo 'ORDENA') ---")
    
    vetor_de_chars = [{'Chave': char} for char in "ORDENA"]

    print("Vetor original: ", end="")
    print_array(vetor_de_chars)

    shellSort(vetor_de_chars)

    print("Vetor ordenado: ", end="")
    print_array(vetor_de_chars)