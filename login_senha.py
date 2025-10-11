def verificar_login():
    login_digitado = input("Informe o seu login: ")
    senha_digitada = input("Informe a sua senha: ")

    login_senha = {
        "admin" : "Farcry34!",
        "gerente" : "12345"
    }  

    if login_digitado in login_senha: 
        senha_salva = login_senha[login_digitado] # Captura o valor do login
        if senha_digitada == senha_salva:
            print("\nLogin efetuado com sucesso!")
        else:
            print("\nLogin ou Senha incorreto!")

    else:
        print("\nLogin ou Senha incorreto!")

if __name__ == "__main__":
    verificar_login()