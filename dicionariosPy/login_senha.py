login_senha = {
    "admin" : 12345,
    "gerente" : "ab@caxi"
}

senha_digitada = 12345
if "admin" in login_senha:
    senha = login_senha["admin"]
    if senha_digitada == senha:
        print("Acesso permitido")
