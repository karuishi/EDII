from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

login_senha = {
    "Admin" : "Farcry34!",
    "Gerente" : "12345"
}

voos = {
    "ED-001" : {
        "Origem" : "Salvador",
        "Destino" : "São Paulo",
        "Preco_ida" : 1200.00,
        "Preco_volta": 1150.00,
        "Milhas" : 1500,
        "Aeronave": "Boeing 737",
        "Total_assentos": 10
    },
    "ED-002" : {
        "Origem" : "Rio de janeiro",
        "Destino" : "Brasília",
        "Preco_ida" : 950.00,
        "Preco_volta": 900.00,
        "Milhas" : 1000,
        "Aeronave": "Airbus A320",
        "Total_assentos": 5
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        if login in login_senha and login_senha[login] == senha:
            return redirect(url_for('listar_voos'))
        else:
            return "Login ou senha incorretos!"
    return render_template('login.html')

@app.route('/voos')
def listar_voos():
    return render_template('voos.html', voos=voos)

if __name__ == '__main__':
    app.run(debug=True)