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
    gerar_codigo_reserva(reservas)
    nome_cliente = input("Informe o nome do cliente: ")
    CPF_cliente = input("Informe o CPF do cliente: ")
    