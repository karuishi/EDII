from reserva_compras import Reservas

def formatar_reserva_arquivo(codigo_reserva, detalhes_reservas):
    codigo = codigo_reserva 
    cliente = detalhes_reservas['Cliente']
    cpf = detalhes_reservas['CPF']

    voos_string = ";".join(detalhes_reservas['Voos'])

    return f"{codigo}, {cliente}, {cpf}, {voos_string}"

def salvar_reserva_arquivo(codigo_reserva, reservas):
    reserva_a_salvar = reservas[codigo_reserva]
    with open("reservas.txt", "a") as arquivo:
        linha_formatada = formatar_reserva_arquivo(codigo_reserva, reserva_a_salvar)
        arquivo.write(f"{linha_formatada}\n")