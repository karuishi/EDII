from flask import Flask, render_template, request, redirect, url_for
import json
import os
from BTree import BTree 
from data_manager import *

app = Flask(__name__, template_folder='../templates', static_folder='../static')

voos = carregar_voos()
dados_clientes, clientes_btree_cpf = carregar_clientes()
reservas = carregar_reservas()
login_senha = carregar_login()

# --- Rotas de Login ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        if login in login_senha and login_senha[login]["senha"] == senha:
            role = login_senha[login]["role"]
            if role == "admin":
                return redirect(url_for('listar_voos')) 
            else :
                return redirect(url_for('pagina_passageiro'))
        else:
            return "Login ou senha incorretos!"
    return render_template('login/login.html')

# --- Rota de registro para novas contas --- 
@app.route('/login/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'GET':
        return render_template('login/criar_conta.html')
    
    if request.method == 'POST':
        novo_login = request.form['login']
        nova_senha = request.form['senha']
        nova_role = request.form.get('role', 'cliente') # .get() evita erro se o campo faltar

        if novo_login in login_senha:
            return "Erro: Login já existe!"
        
        login_senha[novo_login] = {
            "senha" : nova_senha,
            "role" : nova_role
        }
        salvar_login(login_senha)
        return redirect(url_for('login'))

# --- Rota do módulo do passageiro ---
@app.route('/passageiro')
def pagina_passageiro():
    return render_template('passageiros/passageiro.html', voos=voos)

# --- Rotas de Gestão de Voos ---
@app.route('/voos')
def listar_voos():
    return render_template('voos/voos.html', voos=voos)

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
        salvar_voos(voos)
        return redirect(url_for('listar_voos'))
    return render_template('voos/adicionar_voo.html')

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
        salvar_voos(voos)
        return redirect(url_for('listar_voos'))
    return render_template('voos/editar_voo.html', voo=voo, codigo_voo=codigo_voo)

@app.route('/voos/excluir/<codigo_voo>')
def excluir_voo(codigo_voo):
    if codigo_voo in voos:
        del voos[codigo_voo]
        salvar_voos(voos)
    return redirect(url_for('listar_voos'))

# --- Rotas de Gestão de Clientes ---
@app.route('/clientes')
def listar_clientes():
    if not dados_clientes:
        return render_template('clientes/clientes.html', clientes_ordenados=[])
    
    lista_ordenada = sorted(dados_clientes.items(), key=lambda item: item[1]["Nome"])
    return render_template('clientes/clientes.html', clientes_ordenados=lista_ordenada)

@app.route('/clientes/adicionar', methods=['GET', 'POST'])
def adicionar_cliente():
    if request.method == 'POST':
        try:
            cpf = int(request.form['cpf'])
        except ValueError:
            return "Erro: CPF deve conter apenas números."

        if clientes_btree_cpf.search(cpf):
            return "Erro: Cliente com este CPF já cadastrado!"
        
        nome = request.form['nome']
        clientes_btree_cpf.insert(cpf)
        
        dados_clientes[cpf] = {
            "Nome" : nome,
            "Reservas" : [],
            "Data_viagem" : request.form['data_viagem'],
            "Milhas" : request.form['milhas']
        }
        
        salvar_clientes(dados_clientes)
        return redirect(url_for('listar_clientes'))

    return render_template('clientes/adicionar_cliente.html')

@app.route('/clientes/ordenar_cpf')
def listar_clientes_cpf():
    if not dados_clientes:
        return render_template('clientes/clientes.html', clientes_ordenados=[])
        
    cpfs_ordenados = sorted(dados_clientes.keys())
    
    lista_final = []
    for cpf in cpfs_ordenados:
        lista_final.append( (cpf, dados_clientes[cpf]) )
        
    return render_template('clientes/clientes.html', clientes_ordenados=lista_final)

# --- Rotas de Gestão de Reservas ---
@app.route('/reservas')
def listar_reservas():
    return render_template('reservas/reservas.html', reservas=reservas)

@app.route('/reservas/nova', methods=['GET', 'POST'])
def fazer_reserva():
    if request.method == 'GET':
        return render_template('reservas/adicionar_reserva.html', voos=voos, clientes=dados_clientes)

    if request.method == 'POST':
        try:
            cpf_cliente = int(request.form['cpf_cliente'])
        except ValueError:
            return "Erro: Formato de CPF inválido."

        voos_selecionados = request.form.getlist('voos_selecionados')

        if cpf_cliente not in dados_clientes:
            return "Erro: Cliente não encontrado. Cadastre o cliente primeiro."

        if not voos_selecionados:
            return "Erro: Nenhum voo foi selecionado."

        for codigo_voo in voos_selecionados:
            if voos[codigo_voo]['Total_assentos'] <= 0:
                return f"Erro: Não há assentos disponíveis para o voo {codigo_voo}!"

        for codigo_voo in voos_selecionados:
            voos[codigo_voo]['Total_assentos'] -= 1
        salvar_voos(voos)

        novo_codigo = gerar_codigo_reserva(reservas)
        nome_cliente = dados_clientes[cpf_cliente]['Nome']

        reservas[novo_codigo] = {
            "Cliente": nome_cliente,
            "CPF": cpf_cliente,
            "Voos": voos_selecionados
        }
        salvar_reservas(reservas)

        dados_clientes[cpf_cliente]['Reservas'].append(novo_codigo)
        salvar_clientes(dados_clientes)

        return redirect(url_for('listar_reservas'))

if __name__ == '__main__':
    app.run(debug=True)