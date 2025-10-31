def adicionar_voo(voos):
    codigo_voo = input("Informe o código do voo: ")
    origem_voo = input("Informe a origem do voo: ")
    destino_voo = input("Informe o destino do voo: ")

    try:
        milhas_voo = int(input("Informe a quantidade de milhas percorridas durante o voo: "))
        preco_passagem_ida = float(input("Informe o preço da passagem de ida: "))
        preco_passagem_volta = float(input("Informe o preço da passagem de volta: "))
        total_assentos = int(input("Informe o número total de assentos da aeronave: "))
    except ValueError:
        print("\nValor inválido para milhas, preço ou assentos. Apenas número são permitidos.")
        return
    
    tipo_aeronave = input("Informe o tipo da aeronave: ")

    voos[codigo_voo] = {
        "Origem" : origem_voo,
        "Destino" : destino_voo,
        "Preco_ida" : preco_passagem_ida,
        "Preco_volta" : preco_passagem_volta,
        "Milhas" : milhas_voo,
        "Aeronave" : tipo_aeronave,
        "Total_assentos" : total_assentos
    }
    print(f"\nVoo {codigo_voo} adicionado com sucesso!")

def excluir_voo(voos):
    codigo_voo_digitado = input("Informe o código do voo a ser deletado: ")

    if codigo_voo_digitado in voos:
        del voos[codigo_voo_digitado]
        print("\nVoo deletado com sucesso!")
    else:
        print("\nCódigo de voo não encontrado!")

def editar_voo(voos):
    codigo_voo_digitado = input("Informe o código do voo a ser editado: ")
    
    if codigo_voo_digitado not in voos:
        print("\nCódigo de voo não encontrado!")
        return 

    print(f"Dados do voo {codigo_voo_digitado}: {voos[codigo_voo_digitado]}\n")
    dado_atualizado = input("Informe o campo a ser atualizado (ex: origem, destino, preco_ida): ")

    if dado_atualizado in voos[codigo_voo_digitado]:
        novo_valor = input(f"Informe o novo valor para '{dado_atualizado}': ")
        try:
            if dado_atualizado in ["Preco_ida", "Preco_volta"]:
                voos[codigo_voo_digitado][dado_atualizado] = float(novo_valor)
            elif dado_atualizado in ["Milhas", "Total_assentos"]:
                voos[codigo_voo_digitado][dado_atualizado] = int(novo_valor)
            else:
                voos[codigo_voo_digitado][dado_atualizado] = novo_valor 
            print(f"\nCampo '{dado_atualizado}' editado com sucesso!")
        except ValueError:
            print("\nErro: Valor inválido para um campo numérico.")
    else:
        print("\nCampo não encontrado!")

def exibir_menu():
    print("\n--- Menu ---")
    print("1. Adicionar voo")
    print("2. Excluir voo")
    print("3. Editar voo")
    print("4. Sair")

def main():
    voos = {}
    while True:
        exibir_menu()
        escolha = input("Digite um número da sua opção: ")

        if escolha == '1':
            adicionar_voo(voos)
        elif escolha == '2':
            excluir_voo(voos)
        elif escolha == '3':
            editar_voo(voos)
        elif escolha == '4':
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida! Escolha um número de 1 a 4")     

if __name__ == "__main__":
    main()