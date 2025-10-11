from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Nome do arquivo onde salvaremos os dados dos voos
ARQUIVO_VOOS = 'voos.json'

def carregar_voos():
    # Função de Carregar voos do arquivo
    if os.path.exists(ARQUIVO_VOOS):
        with open(ARQUIVO_VOOS, 'r') as f:
            return json.load(f)
    else:
        return {
            "ED-001" : {
             "Origem" : "Salvador", "Destino" : "São Paulo", "Preco_ida" : 1200.00,
             "Preco_volta": 1150.00, "Milhas" : 1500, "Aeronave": "Boeing 737", "Total_assentos": 10
            },
            "ED-002" : {
                "Origem" : "Rio de janeiro", "Destino" : "Brasília", "Preco_ida" : 950.00,
                "Preco_volta": 900.00, "Milhas" : 1000, "Aeronave": "Airbus A320", "Total_assentos": 5
            }
        }

def salvar_voos(voos):
    with open(ARQUIVO_VOOS, 'w') as f:
        json.dump(voos, f, indent=4)

login_senha = {
    "Admin" : "Farcry34!",
    "Gerente" : "12345"
}

voos = carregar_voos()

# Rota principal para a página de login
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

# Rota para listar os voos
@app.route('/voos')
def listar_voos():
    return render_template('voos.html', voos=voos)

# Rota para adicionar um novo voo
@app.route('/voos/adicionar', methods=['GET', 'POST'])
def adicionar_voo():
    if request.method == 'POST':
        codigo_voo = request.form['codigo']
        voos[codigo_voo] = {
            "Origem" : request.form['origem'],
            "Destino" : request.form['destino'],
            "Preco_ida" : float(request.form['preco_ida']),
            "Preco_volta": float(request.form['preco_volta']),
            "Milhas" : int(request.form['milhas']),
            "Aeronave": request.form['aeronave'],
            "Total_assentos": int(request.form['total_assentos'])
        }
        salvar_voos(voos) # Salva após add
        return redirect(url_for('listar_voos'))
    return render_template('adicionar_voo.html')

# Rota para editar um voo
@app.route('/voos/editar/<codigo_voo>', methods=['GET', 'POST'])
def editar_voo(codigo_voo):
    voo = voos.get(codigo_voo)
    if request.method == 'POST':
        voo['Origem'] = request.form['origem']
        voo['Destino'] = request.form['destino']
        voo['Preco_ida'] = float(request.form['preco_ida'])
        voo['Preco_volta'] = float(request.form['preco_volta'])
        voo['Milhas'] = int(request.form['milhas'])
        voo['Aeronave'] = request.form['aeronave']
        voo['Total_assentos'] = int(request.form['total_assentos'])
        salvar_voos(voos) # Salva após editar
        return redirect(url_for('listar_voos'))
    return render_template('editar_voo.html', voo=voo, codigo_voo=codigo_voo)

# Rota para excluir um voo
@app.route('/voos/excluir/<codigo_voo>')
def excluir_voo(codigo_voo):
    if codigo_voo in voos:
        del voos[codigo_voo]
        salvar_voos(voos) # Salva após excluir
    return redirect(url_for('listar_voos'))

if __name__ == '__main__':
    app.run(debug=True)