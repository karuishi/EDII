# Adicionamos o caminho da pasta EDII para que o Python encontre os módulos
import sys
sys.path.append('EDII')

from reserva_compras.Reservas import efetuar_reserva

def main():
    voos = {
        "ED-001" : {
            "origem" : "Salvador",
            "destino" : "São Paulo",
            "preco_ida" : 1200.00,
            "preco_volta": 1150.00,
            "milhas" : 1500,
            "aeronave": "Boeing 737",
            "total_assentos": 10 
        },
        "ED-002" : {
            "origem" : "Rio de janeiro",
            "destino" : "Brasília",
            "preco_ida" : 950.00,
            "preco_volta": 900.00,
            "milhas" : 1000,
            "aeronave": "Airbus A320",
            "total_assentos": 5 
        }
    }

    reservas = {} # Inicializa o dicionário de reservas como vazio

    print("--- Iniciando Teste do Sistema de Reservas ---")
    efetuar_reserva(reservas, voos)

    print("\n--- Resultado Final ---")
    print("Reservas existentes:", reservas)
    print("Status dos assentos nos voos:", voos)

if __name__ == "__main__":
    main()