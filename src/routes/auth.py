from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.database import login_senha, dados_clientes, clientes_btree_cpf
from src.models.data_manager import salvar_login, salvar_clientes
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        if login in login_senha and check_password_hash(login_senha[login]["senha"], senha):
            session['usuario'] = login
            session['role'] = login_senha[login]["role"]

            if 'cpf' in login_senha[login]:
                session['cpf'] = login_senha[login]['cpf']
            
            role = session['role']

            if role == 'admin':
                return redirect(url_for('admin.listar_voos'))
            else : 
                return redirect(url_for('passageiro.pagina_passageiro'))
            
        else:
            flash('Login ou senha incorretos!', 'danger')
            return render_template('login/login.html')
        
    return render_template('login/login.html')

@auth_bp.route('/login/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'GET':
        return render_template('login/criar_conta.html')
    
    if request.method == 'POST':
        novo_login = request.form['login']
        nova_senha = request.form['senha']
        nova_role = request.form.get('role', 'cliente') 
        cpf_digitado = request.form.get('cpf')

        if novo_login in login_senha:
            flash('Login já existe!', 'danger')
            return redirect(url_for('auth.criar_conta'))

        if nova_role == 'cliente':
            if not cpf_digitado:
                 flash('CPF é obrigatório!', 'danger')
                 return redirect(url_for('auth.criar_conta'))
            try:
                cpf_int = int(cpf_digitado)
                if not clientes_btree_cpf.buscar(cpf_int):
                    clientes_btree_cpf.inserir(cpf_int)
                    nome_cliente = request.form.get('nome','passageiro')
                    dados_clientes[cpf_int] = {
                        "Nome": nome_cliente,
                        "Reservas": [],
                        "Data_viagem":"",
                        "Milhas": 0
                    }
                    salvar_clientes(dados_clientes)
            except ValueError:
                flash('CPF inválido', 'danger')
                return redirect(url_for('auth.criar_conta'))
        
        cpf_para_salvar = cpf_digitado if nova_role == 'cliente' else None

        login_senha[novo_login] = {
            "senha" : generate_password_hash(nova_senha),
            "role" : nova_role,
            "cpf": cpf_para_salvar
        }
        salvar_login(login_senha)
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))