voos = {
    "ED-001" : { # A chave é o código do voo
    # O valor é outro dicionário com os detalhes do voo
        "origem" : "Salvador",
        "destino" : "São Paulo",
        "preco" : 1200.00,
        "milhas" : 1500
    },

    "ED-002" : {
        "origem" : "Rio de janeiro",
        "destino" : "Brasília",
        "preco" : 950.00,
        "milhas" : 1000
    }
}

preco_voos = voos["ED-001"]["preco"]
print(preco_voos)

destino_voos = voos["ED-002"]["destino"]
print(destino_voos)