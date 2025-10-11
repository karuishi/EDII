from reserva_compras import Arquivos
from voos import GestaoVoos

reservas = {
    "RES01" : {
        "Cliente" : "Ana",
        "CPF" : "123.456.789-00",
        "voos" : ["ED-001"]
    }
}

def gerar_codigo_reserva(reservas):
    prox_codigo = len(reservas) + 1
    return f"RES{prox_codigo}" # A f-string permite que você coloque variáveis diretamente dentro 
                                # de uma string, e o Python cuida da conversão para você.

def efetuar_reserva(reservas, voos):
    codigo_reserva = gerar_codigo_reserva(reservas)
    nome_cliente = input("Informe o nome do cliente: ")
    CPF_cliente = input("Informe o CPF do cliente: ")
    lista_voos = []
    
    while True:
        print("\nVoos disponíveis: ", list(voos.keys()))
        codigo_voo = input("Digite o código do voo a ser adicionado (ou 'fim' para terminar): ")

        if codigo_voo == 'fim':
            if not lista_voos: 
                print("\nNenhum voo foi selecionado. Reserva cancelada.")
                return 
            break
        
        if codigo_voo in voos:
            if voos[codigo_voo]['total_assentos'] > 0:
                lista_voos.append(codigo_voo)
                print(f"Voo {codigo_voo} adicionado à reserva!")
            else:
                print(f"\nNão há assentos disponíveis para o voo {codigo_voo}. Operação cancelada!")
                return
        else:
            print("Código de voo inválido. Tente novamente.")
        
    for voo_confirmado in lista_voos:
        voos[voo_confirmado]['total_assentos'] -= 1
    
    reservas[codigo_reserva] = {
        "Cliente" : nome_cliente,
        "CPF" : CPF_cliente,
        "Voos" : lista_voos
    }

    print(f"\nReserva {codigo_reserva} criada com sucesso para {nome_cliente}!")
    Arquivos.salvar_reserva_arquivo(codigo_reserva, reservas)