import pandas as pd
import time
import sys

def quickSortFirst(vetor):
    if len(vetor) <= 1:
        return vetor
    else:
        pivo = vetor[0]
        menores = [x for x in vetor[1:] if x <= pivo]
        maiores = [x for x in vetor[1:] if x > pivo]
        return quickSortFirst(menores) + [pivo] + quickSortFirst(maiores)

def quickSortCentral(vetor):
    if len(vetor) <= 1:
        return vetor
    else:
        indice_central = len(vetor) // 2
        pivo = vetor[indice_central]
        listaSemPivo = vetor[:indice_central] + vetor[indice_central+1:]
        menores = [x for x in listaSemPivo if x <= pivo]
        maiores = [x for x in listaSemPivo if x > pivo]
        return quickSortCentral(menores) + [pivo] + quickSortCentral(maiores)

def heapIfy(vetor, n, i):
    maior = i # Inicializa o maior como a raiz
    esq = 2 * i + 1
    dir = 2 * i + 2

    # Verifica se o filho da esquerda existe e é maior que a raiz
    if esq < n and vetor[esq] > vetor[maior]:
        maior = esq
    # Verifica se o filho da direita existe e é maior que o maior atual
    if dir < n and vetor[dir] > vetor[maior]:
        maior = dir
    # Muda a raiz se necessário
    if maior != i:
        vetor[i], vetor[maior] = vetor[maior], vetor[i]
        heapIfy(vetor, n, maior)

def heapSort(vetor):
    n = len(vetor)
    for i in range(n // 2 - 1, -1, -1):
        heapIfy(vetor, n, i)
        
    # Extrai um por um os elementos do heap
    for i in range(n - 1, 0, -1):
        vetor[i], vetor[0] = vetor[0], vetor[i] # Move a raiz atual para o fim
        heapIfy(vetor, i, 0)
    return vetor

try:
    # Carrega o conjunto de dados
    df = pd.read_csv('ai_assistant_usage_student_life.csv')

    # Seleciona a coluna para ordenar e converte para lista
    colunaOrdenar = 'SessionLengthMin'
    dados = df[colunaOrdenar].dropna().tolist() # .dropna() remove valores nulos

    # Cria cópias dos dados para cada algoritmo
    dadosQSFirst = list(dados)
    dadosQSCentral = list(dados)
    dadosHeap = list(dados)

    print(f"Coluna selecionada para ordenação: '{colunaOrdenar}'")
    print(f"Total de registros a serem ordenados: {len(dados)}")
    print("-" * 40)
    
    # --- QuickSortFirst ---
    inicio = time.time()
    dados_ordenados_qsfirst = quickSortFirst(dadosQSFirst) 
    fim = time.time()
    tempoQSFirst = fim - inicio

    # --- QuickSortCentral ---
    inicio = time.time()
    dados_ordenados_qscentral = quickSortCentral(dadosQSCentral) 
    fim = time.time()
    tempoQSCentral = fim - inicio

    # --- HeapSort ---
    # HeapSort modifica a lista original (in-place), então não precisa de uma nova variável
    inicio = time.time()
    heapSort(dadosHeap) # A lista 'dadosHeap' agora está ordenada
    fim = time.time()
    tempoHeapSort = fim - inicio

    # --- Impressão dos Tempos de Execução ---
    print("Resultados de Desempenho:")
    print(f"  - Tempo QuickSortFirst:  {tempoQSFirst:.6f} segundos")
    print(f"  - Tempo QuickSortCentral: {tempoQSCentral:.6f} segundos")
    print(f"  - Tempo HeapSort:        {tempoHeapSort:.6f} segundos")
    print("-" * 40)

    # --- Impressão da Amostra dos Dados Ordenados ---
    print("Verificação da Ordenação (10 primeiros e últimos elementos):\n")

    print("QuickSort (Pivô Primeiro):")
    print(f"  Primeiros: {dados_ordenados_qsfirst[:10]}")
    print(f"  Últimos:   {dados_ordenados_qsfirst[-10:]}\n")

    print("QuickSort (Pivô Central):")
    print(f"  Primeiros: {dados_ordenados_qscentral[:10]}")
    print(f"  Últimos:   {dados_ordenados_qscentral[-10:]}\n")

    print("HeapSort:")
    print(f"  Primeiros: {dadosHeap[:10]}")
    print(f"  Últimos:   {dadosHeap[-10:]}\n")


except FileNotFoundError:
    print("Erro: O arquivo 'ai_assistant_usage_student_life.csv' não foi encontrado.")
    print("Por favor, verifique se o arquivo está na mesma pasta que o seu script Python.")
except KeyError:
    print(f"Erro: A coluna '{colunaOrdenar}' não foi encontrada no arquivo CSV.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")