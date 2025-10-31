from flask.BTree import BTree

def adicionar_cliente(btree, dados):
    """
    Adiciona um novo cliente.
    Usa btree.search() para verificar se o CPF já existe.
    Usa btree.insert() para adicionar o novo CPF ao índice.
    """
    try:
        CPF_novo_cliente = int(input("Informe o CPF do novo cliente (apenas números): ")) 
    except ValueError:
        print("\nErro: CPF deve conter apenas números.")
        return

    # 1. USA A BUSCA DA ÁRVORE B 
    if btree.search(CPF_novo_cliente):
        print("\nCliente já cadastrado! Tente um novo CPF.")
        return
    else:
        # 2. Pede os outros dados
        nome_novo_cliente = input("Informe o nome do novo cliente: ")
        data_viagem = input("Informe a data da viagem (DD/MM/AAAA): ")
        milhas = input("Informe a quantidade de milhas: ")

        # 3. INSERE NAS DUAS ESTRUTURAS
        # A. Insere na arvore B
        btree.insert(CPF_novo_cliente) 
        
        # B. Insere no Dicionário de dados
        dados[CPF_novo_cliente] = {
            "Nome" : nome_novo_cliente,
            "Reservas" : [], # Começa com uma lista de reservas vazia
            "Data_viagem" : data_viagem,
            "Milhas" : milhas
        }

        print(f"\nCliente {nome_novo_cliente} adicionado com sucesso!")

def consulta_OrdenadaCPF(btree, dados):
    """
    Lista todos os clientes ordenados por CPF.
    Usa a função 'traverse' da Árvore B, que já é ordenada.
    """
    btree.traverse(dados)

# --- FUNÇÕES QUE USAM O DICIONÁRIO (NÃO OTIMIZADAS PELA ÁRVORE DE CPF) ---

def consulta_OrdenadaNome(dados):
    """
    Lista os clientes ordenados por Nome.
    Isto não pode ser otimizado pela Árvore B de CPFs.
    """
    if not dados:
        print("\nNão há clientes cadastrados.")
        return

    # Usa o método lambda para ordenar pelos nomes dentro do dicionário
    try:
        nome_ordenado = sorted(dados.items(), key=lambda item: item[1]["Nome"])
    except KeyError:
        print("\nErro nos dados: Chave 'Nome' não encontrada.")
        return

    print("\n--- Clientes Ordenados por Nome ---")
    for cpf, dados_cliente in nome_ordenado:
        print(f"Nome: {dados_cliente['Nome']} | CPF: {cpf} | Milhas: {dados_cliente['Milhas']}")

def busca_nome(dados):
    """
    Procura um cliente por nome específico.
    """
    if not dados:
        print("\nNão há clientes cadastrados.")
        return
        
    nome_digitado = input("Informe o nome a ser buscado: ")
    encontrado = False

    for cpf, dados_cliente in dados.items():
        if nome_digitado.lower() == dados_cliente["Nome"].lower():
            print(f"\nEncontrado: Nome: {dados_cliente['Nome']} | CPF: {cpf} | Milhas: {dados_cliente['Milhas']}")
            encontrado = True
            
    if not encontrado:
        print("\nNome não encontrado!")

def busca_inicial_nome(dados):
    """
    Lista clientes pela inicial do nome.
    """
    if not dados:
        print("\nNão há clientes cadastrados.")
        return
        
    inicial_digitada = input("Informe a inicial a ser buscada: ")
    encontrado = False

    for cpf, dados_cliente in dados.items():
        # Verifica se o nome não está vazio antes de aceder a [0]
        if dados_cliente["Nome"] and inicial_digitada.lower() == dados_cliente["Nome"][0].lower():
            print(f"Nome: {dados_cliente['Nome']} | CPF: {cpf} | Milhas: {dados_cliente['Milhas']}")
            encontrado = True
    
    if not encontrado:
        print("\nNenhum cliente encontrado com essa inicial.")

def main():
    # 1. O dicionário
    dados_clientes = {} 

    # 2. O "índice rápido" (guarda SÓ os CPFs para busca rápida)
    #    Criamos uma Árvore B com grau mínimo 3 
    clientes_btree_cpf = BTree(t=3)
    
    # Adiciona alguns dados de exemplo
    clientes_btree_cpf.insert(12345678900)
    dados_clientes[12345678900] = {"Nome": "Ana Silva", "Reservas": [], "Data_viagem": "10/11/2025", "Milhas": 1200}
    clientes_btree_cpf.insert(98765432100)
    dados_clientes[98765432100] = {"Nome": "Bruno Costa", "Reservas": [], "Data_viagem": "12/11/2025", "Milhas": 800}
    clientes_btree_cpf.insert(55566677700)
    dados_clientes[55566677700] = {"Nome": "Carla Dias", "Reservas": [], "Data_viagem": "15/11/2025", "Milhas": 2500}


    while True:
        print("\n--- Gestão de Clientes (Otimizada com B-Tree) ---")
        print("1. Adicionar Cliente (Otimizado)")
        print("2. Listar Clientes (Ordenado por CPF - Otimizado)")
        print("3. Listar Clientes (Ordenado por Nome)")
        print("4. Buscar Cliente (por Nome Específico)")
        print("5. Listar Clientes (por Inicial do Nome)")
        print("6. Sair")
        
        escolha = input("Digite a sua opção: ")

        if escolha == '1':
            adicionar_cliente(clientes_btree_cpf, dados_clientes)
        elif escolha == '2':
            consulta_OrdenadaCPF(clientes_btree_cpf, dados_clientes)
        elif escolha == '3':
            consulta_OrdenadaNome(dados_clientes)
        elif escolha == '4':
            busca_nome(dados_clientes)
        elif escolha == '5':
            busca_inicial_nome(dados_clientes)
        elif escolha == '6':
            print("\nA sair da Gestão de Clientes...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

# Executa o menu principal
if __name__ == "__main__":
    main()