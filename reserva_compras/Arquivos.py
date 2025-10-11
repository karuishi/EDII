from reserva_compras import Reservas

def formatar_reserva_arquivo(codigo_reserva, reservas):
    codigo = codigo_reserva 
    cliente = reservas['Cliente']
    cpf = reservas['CPF']

    voos_string = ";".join(reservas['voos'])

    return f"{codigo}, {cliente}, {cpf}, {voos_string}"

def salvar_reserva_arquivo(codigo_reserva, reservas):
    with open("reservas.txt", "a") as arquivo:
        arquivo.write(f"{formatar_reserva_arquivo(codigo_reserva, reservas)}\n")