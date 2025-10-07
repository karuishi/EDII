def adicionar_voo(voos):
    codigo_voo = input("Informe o código do voo: ")
    origem_voo = input("Informe a origem do voo: ")
    destino_voo = input("Informe o destino do voo: ")
    milhas_voo = input("Informe a quantidade de milhas percorridas durante o voo: ")
    preco_passagem_ida = input("Informe o preço da passagem de ida: ")
    preco_passagem_volta = input("Informe o preço da passagem de volta: ")
    tipo_aeronave = input("Informe o tipo da aeronave: ")
    total_assentos = input("Informe o número total de assentos da aeronave: ")

    voos[codigo_voo] = {
        "origem" : origem_voo,
        "destino" : destino_voo,
        "preco_ida" : preco_passagem_ida,
        "preco_volta" : preco_passagem_volta,
        "milhas" : milhas_voo,
        "aeronave" : tipo_aeronave,
        "total_assentos" : total_assentos
    }
    print(f"\nVoo {codigo_voo} adicionado com sucesso!")

    # origem_voo_salva = voos[codigo_voo][origem_voo]
    # destino_voo_salva = voos[codigo_voo][destino_voo]
    # preco_ida_salva = voos[codigo_voo][preco_passagem_ida]
    # preco_volta_salva = voos[codigo_voo][preco_passagem_volta]
    # milhas_salva = voos[codigo_voo][milhas_voo]
    # print(origem_voo_salva)
    # print(destino_voo_salva)
    # print(preco_ida_salva)
    # print(preco_volta_salva)
    # print(milhas_salva)
    # print(preco_ida_salva + preco_volta_salva)

def excluir_voo(voos):
    codigo_voo_digitado = input("Informe o código do voo a ser deletado: ")

    if codigo_voo_digitado in voos:
        del voos[codigo_voo_digitado]
        print("\nVoo deletado com sucesso!")
    else:
        print("\nCódigo de voo não encontrado!")

def editar_voo(voos):
    codigo_voo_digitado = input("Informe o código do voo a ser editado: ")
    dado_atualizado = input("Informe o dado a ser atualizado: ")
    novo_valor = input("Informe o novo valor: ")
    
    if codigo_voo_digitado in voos:
        if dado_atualizado in voos[codigo_voo_digitado]:
            voos[codigo_voo_digitado][dado_atualizado] = novo_valor
            print(f"\n{dado_atualizado} editado com sucesso!")
        else:
            print("\nDado não encontrado!")
    else:
        print("\nCódigo de voo não encontrado!")