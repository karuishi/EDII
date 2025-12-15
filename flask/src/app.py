from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from BTree import BTree 
from data_manager import *
import random

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'chave_secreta_ed2'

voos = carregar_voos()
dados_clientes, clientes_btree_cpf = carregar_clientes()
reservas = carregar_reservas()
login_senha = carregar_login()

# --- Rota da Paǵina Inicial ---
@app.route('/')
def home():
    return render_template('tela_inicial/home.html', voos=voos)

# --- Rotas de Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        if login in login_senha and login_senha[login]["senha"] == senha:
            session['usuario'] = login
            session['role'] = login_senha[login]["role"]

            if 'cpf' in login_senha[login]:
                session['cpf'] = login_senha[login]['cpf']
            
            role = session['role']

            if role == 'admin':
                return redirect(url_for('listar_voos')) # Criar uma página para adm
            else : 
                return redirect(url_for('pagina_passageiro'))
            
        else:
            flash('Login ou senha incorretos!', 'danger')
            return render_template('login/login.html')
        
    return render_template('login/login.html')

# --- Rota de registro para novas contas --- 
@app.route('/login/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'GET':
        return render_template('login/criar_conta.html')
    
    if request.method == 'POST':
        novo_login = request.form['login']
        nova_senha = request.form['senha']
        nova_role = request.form.get('role', 'cliente') # Pega a role (se não vier, assume cliente)
        cpf_digitado = request.form.get('cpf')

        if novo_login in login_senha:
            flash('Login já existe!', 'danger')
            return redirect(url_for('criar_conta'))

        if nova_role == 'cliente':
            if not cpf_digitado:
                 flash('CPF é obrigatório!', 'danger')
                 return redirect(url_for('criar_conta'))
            try:
                cpf_int = int(cpf_digitado)
                # Verifica se já existe na árvore B
                if not clientes_btree_cpf.search(cpf_int):
                    clientes_btree_cpf.insert(cpf_int)
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
                return redirect(url_for('criar_conta'))
        cpf_para_salvar = cpf_digitado if nova_role == 'cliente' else None

        login_senha[novo_login] = {
            "senha" : nova_senha,
            "role" : nova_role,
            "cpf": cpf_para_salvar
        }
        salvar_login(login_senha)
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Rota do módulo do passageiro ---
@app.route('/passageiro')
def pagina_passageiro():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    cpf_sessao = session.get('cpf')

    if role == 'admin':
        dados_do_clientes = {"Nome": "ADM", "Milhas": "∞"}
        cpf_atual = 0
    else:
        if not cpf_sessao:
            return redirect(url_for('logout'))
        try:
            cpf_atual = int(cpf_sessao)
            dados_do_clientes = dados_clientes.get(cpf_atual)
            if not dados_do_clientes:
                flash("Dados do cliente não encontrado", 'danger')
                return redirect(url_for('login'))
        except ValueError:
            return redirect(url_for('logout'))
    
    cpf_sessao = session.get('cpf')
    if not cpf_sessao:
        return redirect(url_for('logout'))
    
    try:
        cpf_atual = int(cpf_sessao)
    except ValueError:
        return redirect(url_for('logout'))
    
    dados_do_clientes = dados_clientes.get(cpf_atual)
    if not dados_clientes:
        flash("Dados do cliente não encontrado", 'danger')
    
    origem_filtro = request.args.get('origem')
    destino_filtro = request.args.get('destino')
    data_ida_filtro = request.args.get('data_ida')

    voos_exibicao = {}
    
    if origem_filtro and destino_filtro or data_ida_filtro:
        for codigo, dados in voos.items():
            corresponde = True
            if origem_filtro and dados['Origem'].lower() != origem_filtro.lower():
                corresponde = False
            
            if corresponde and destino_filtro and dados['Destino'].lower() != destino_filtro.lower():
                corresponde = False
            
            if corresponde and data_ida_filtro:
                datas_disponiveis = dados.get('Datas', [])
                if data_ida_filtro not in datas_disponiveis:
                    corresponde = False
            
            if corresponde:
                voos_exibicao[codigo] = dados
    else:
        voos_exibicao = voos
    
    # Filtrar reservas do cliente logado
    minhas_reservas = {}
    if role != 'admin':
        for codigo, reserva in reservas.items():
            if int(reserva['CPF']) == cpf_atual:
                minhas_reservas[codigo] = reserva

    return render_template(
        'passageiros/dashboard.html', 
        voos = voos_exibicao,
        reservas = minhas_reservas,
        cliente = dados_do_clientes,
        filtros = {'origem': origem_filtro, 'destino': destino_filtro}
        )

@app.route('/passageiro/reservar/<codigo_voo>')
def reservar_passagem(codigo_voo):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') == 'admin':
        flash('Admins devem usar o painel administrativo para criar reservas.', 'warning')
        return redirect(url_for('pagina_passageiro'))
    
    if 'cpf' not in session:
        return redirect(url_for('login'))

    cpf_cliente = int(session['cpf'])

    # Verifica se o voo existe e tem assentos
    if codigo_voo not in voos:
        flash("Voo não encontrado.", 'danger')
        return redirect(url_for('pagina_passageiro'))
    
    if voos[codigo_voo]['Total_assentos'] <= 0:
        flash("Voo lotado!", 'danger')
        return redirect(url_for('pagina_passageiro'))
    
    # Realiza a reserva
    voos[codigo_voo]['Total_assentos'] -= 1
    salvar_voos(voos)

    novo_codigo_reserva = gerar_codigo_reserva(reservas)
    reservas[novo_codigo_reserva] = {
        "Cliente": dados_clientes[cpf_cliente]['Nome'],
        "CPF": cpf_cliente,
        "Voos": [codigo_voo]
    }
    salvar_reservas(reservas)

    # Atualiza o cliente
    dados_clientes[cpf_cliente]['Reservas'].append(novo_codigo_reserva)
    milhas_ganhas = voos[codigo_voo]['Milhas']
    milhas_atuais = int(dados_clientes[cpf_cliente].get('Milhas', 0))
    dados_clientes[cpf_cliente]['Milhas'] = milhas_atuais + milhas_ganhas

    datas_do_voo = voos[codigo_voo].get('Datas', [])
    if datas_do_voo:
        dados_clientes[cpf_cliente]['Data_viagem'] = datas_do_voo[0]

    salvar_clientes(dados_clientes)

    flash(f'Reserva {novo_codigo_reserva} realizada com sucesso!', 'success')
    return redirect(url_for('pagina_passageiro'))

# ==============================================================================
# --- ROTAS ADMINISTRATIVAS (PROTEGIDAS) ---
# ==============================================================================

# --- Rotas de Gestão de Voos ---
@app.route('/voos')
def listar_voos():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    return render_template('voos/voos.html', voos=voos)

@app.route('/voos/adicionar', methods=['GET', 'POST'])
def adicionar_voo():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    if request.method == 'POST':
        codigo_voo = request.form['codigo']
        
        data = request.form.get('data')
        lista_datas = [data] if data else []

        preco_str = request.form['preco'].replace(',', '.')

        voos[codigo_voo] = {
            "Origem" : request.form['origem'],
            "Destino" : request.form['destino'],
            "Preco" : float(preco_str),
            "Milhas" : int(request.form['milhas']),
            "Aeronave": request.form['aeronave'],
            "Total_assentos": int(request.form['total_assentos']),
            "Datas": lista_datas
        }
        salvar_voos(voos)
        return redirect(url_for('listar_voos'))
    return render_template('voos/adicionar_voo.html')

@app.route('/voos/editar/<codigo_voo>', methods=['GET', 'POST'])
def editar_voo(codigo_voo):
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    voo = voos.get(codigo_voo)
    if request.method == 'POST':
        # --- CORREÇÃO: A linha abaixo foi movida para cá ---
        preco_str = request.form['preco'].replace(',', '.')
        voo['Origem'] = request.form['origem']
        voo['Destino'] = request.form['destino']
        voo['Preco'] = float(preco_str)
        voo['Milhas'] = int(request.form['milhas'])
        voo['Aeronave'] = request.form['aeronave']
        voo['Total_assentos'] = int(request.form['total_assentos'])

        data = request.form.get('data')
        if data:
            voo['Datas'] = [data]
        salvar_voos(voos)
        return redirect(url_for('listar_voos'))
    return render_template('voos/editar_voo.html', voo=voo, codigo_voo=codigo_voo)

@app.route('/voos/excluir/<codigo_voo>')
def excluir_voo(codigo_voo):
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    for res in reservas.values():
        if codigo_voo in res['Voos']:
            flash(f'Não é possível excluir o voo {codigo_voo} pois existem reservas associadas a ele.', 'danger')
            return redirect(url_for('listar_voos'))
    
    if codigo_voo in voos:
        del voos[codigo_voo]
        salvar_voos(voos)
        flash('Voo excluído com sucesso.', 'success')
    
    return redirect(url_for('listar_voos'))

# --- Rotas de Gestão de Clientes ---
@app.route('/clientes')
def listar_clientes():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    if not dados_clientes:
        return render_template('clientes/clientes.html', clientes_ordenados=[])
    
    busca_nome = request.args.get('busca_nome')
    busca_inicial = request.args.get('busca_inicial')

    lista_filtrada = []

    if busca_nome:
        for cpf, dados in dados_clientes.items():
            if busca_nome.lower() in dados['Nome'].lower():
                lista_filtrada.append((cpf, dados))
    elif busca_inicial:
        for cpf, dados in dados_clientes.items():
            if dados['Nome'] and dados['Nome'][0].upper() == busca_inicial.upper():
                lista_filtrada.append((cpf, dados))
    else:
        lista_filtrada = list(dados_clientes.items())

    lista_ordenada = sorted(lista_filtrada, key=lambda item: item[1]["Nome"])
    return render_template('clientes/clientes.html', clientes_ordenados=lista_ordenada)

@app.route('/clientes/adicionar', methods=['GET', 'POST'])
def adicionar_cliente():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
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
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    if not dados_clientes:
        return render_template('clientes/clientes.html', clientes_ordenados=[])
        
    cpfs_ordenados = clientes_btree_cpf.in_order_list()
    
    lista_final = []
    for cpf in cpfs_ordenados:
        if cpf in dados_clientes:
            lista_final.append((cpf, dados_clientes[cpf]))
        
    return render_template('clientes/clientes.html', clientes_ordenados=lista_final)

# --- Rotas de Gestão de Reservas ---
@app.route('/reservas')
def listar_reservas():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    return render_template('reservas/reservas.html', reservas=reservas)

@app.route('/reservas/nova', methods=['GET', 'POST'])
def fazer_reserva():
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
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
                flash(f'Reserva não concluída: O voo {codigo_voo} está esgotado!', 'danger')
                return redirect(url_for('fazer_reserva'))
        
        total_milhas_novas = 0
        proxima_data_encontrada = ""

        for codigo_voo in voos_selecionados:
            voos[codigo_voo]['Total_assentos'] -= 1
            total_milhas_novas += voos[codigo_voo]['Milhas']

            if not proxima_data_encontrada:
                datas = voos[codigo_voo].get('Datas', [])
                if datas:
                    proxima_data_encontrada = datas[0]
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
        milhas_atuais = int(dados_clientes[cpf_cliente].get('Milhas', 0))
        dados_clientes[cpf_cliente]['Milhas'] = milhas_atuais + total_milhas_novas
        if proxima_data_encontrada:
            dados_clientes[cpf_cliente]['Data_viagem'] = proxima_data_encontrada
        salvar_clientes(dados_clientes)

        flash(f'Reserva {novo_codigo} realizada com sucesso para {nome_cliente}!', 'success')
        return redirect(url_for('fazer_reserva'))

# flask/src/app.py

# --- Rota para Ver Detalhes da Reserva ---
@app.route('/reservas/detalhes/<codigo_reserva>')
def detalhes_reserva(codigo_reserva):
    # Verifica se a reserva existe
    reserva = reservas.get(codigo_reserva)
    if not reserva:
        flash('Reserva não encontrada.', 'danger')
        if session.get('role') == 'admin':
            return redirect(url_for('listar_reservas'))
        else:
            return redirect(url_for('pagina_passageiro'))

    # VERIFICAÇÃO DE SEGURANÇA:
    # Permite acesso se for Admin OU se o CPF da reserva for igual ao do usuário logado
    eh_admin = session.get('role') == 'admin'
    cpf_usuario = session.get('cpf')
    eh_dono = cpf_usuario and int(cpf_usuario) == int(reserva['CPF'])

    if not (eh_admin or eh_dono):
        flash('Acesso negado a esta reserva.', 'danger')
        return redirect(url_for('pagina_passageiro'))
    
    # Prepara os dados detalhados
    detalhes_voos = []
    total_preco = 0
    total_milhas = 0
    
    for codigo_voo in reserva['Voos']:
        if codigo_voo in voos:
            v = voos[codigo_voo]
            detalhes_voos.append({
                'codigo': codigo_voo,
                'origem': v['Origem'],
                'destino': v['Destino'],
                'data': v.get('Datas', ['--'])[0], 
                'aeronave': v['Aeronave'],
                'preco': v['Preco'],
                'milhas': v['Milhas']
            })
            total_preco += v['Preco']
            total_milhas += v['Milhas']
            
    return render_template('reservas/detalhes_reserva.html', 
                           reserva=reserva, 
                           codigo=codigo_reserva, 
                           voos=detalhes_voos, 
                           total_preco=total_preco,
                           total_milhas=total_milhas)

# --- Rota para Cancelar Reserva ---
@app.route('/reservas/excluir/<codigo_reserva>')
def excluir_reserva(codigo_reserva):
    if session.get('role') != 'admin':
        return redirect(url_for('pagina_passageiro'))
    
    reserva = reservas.get(codigo_reserva)
    if not reserva:
        flash('Reserva não encontrada.', 'danger')
        return redirect(url_for('listar_reservas'))
    
    cpf_cliente = int(reserva['CPF'])
    voos_reserva = reserva['Voos']
    
    # 1. Devolve os assentos aos voos
    milhas_a_remover = 0
    for codigo_voo in voos_reserva:
        if codigo_voo in voos:
            voos[codigo_voo]['Total_assentos'] += 1
            milhas_a_remover += voos[codigo_voo]['Milhas']
    salvar_voos(voos)
    
    # 2. Atualiza o Cliente (Remove do histórico e estorna as milhas)
    if cpf_cliente in dados_clientes:
        cliente = dados_clientes[cpf_cliente]
        
        # Remove o código da lista de reservas
        if codigo_reserva in cliente['Reservas']:
            cliente['Reservas'].remove(codigo_reserva)
            
        # Subtrai as milhas ganhas (sem deixar ficar negativo)
        milhas_atuais = int(cliente.get('Milhas', 0))
        cliente['Milhas'] = max(0, milhas_atuais - milhas_a_remover)
        
        salvar_clientes(dados_clientes)
        
    # 3. Exclui a reserva do sistema
    del reservas[codigo_reserva]
    salvar_reservas(reservas)
    
    flash(f'Reserva {codigo_reserva} cancelada com sucesso. Assentos liberados.', 'success')
    return redirect(url_for('listar_reservas'))

# --- Rota de Processamento de Check-in ---
@app.route('/checkin', methods=['POST'])
def realizar_checkin():
    codigo_reserva = request.form.get('codigo_reserva')
    
    # 1. Validação Básica
    if not codigo_reserva:
        flash('Por favor, digite o código da reserva.', 'warning')
        return redirect(url_for('pagina_passageiro'))
    
    # Normaliza para maiúsculo (caso o usuário digite 'res1')
    codigo_reserva = codigo_reserva.upper()

    reserva = reservas.get(codigo_reserva)
    
    # 2. Verifica se reserva existe
    if not reserva:
        flash(f'Reserva {codigo_reserva} não encontrada.', 'danger')
        return redirect(url_for('pagina_passageiro') + '#checkin') # Volta pra aba de checkin

    # 3. Verifica se é do usuário logado (Segurança)
    # Se for admin, pode fazer check-in de qualquer um
    if session.get('role') != 'admin':
        cpf_logado = session.get('cpf')
        if not cpf_logado or int(reserva['CPF']) != int(cpf_logado):
             flash('Você só pode fazer check-in das suas próprias reservas.', 'danger')
             return redirect(url_for('pagina_passageiro') + '#checkin')

    # 4. Lógica de Check-in (Gerar Assento e Status)
    # Se já tiver assento, mantém. Se não, gera um novo.
    if 'Assentos' not in reserva:
        reserva['Assentos'] = {}
        for voo in reserva['Voos']:
            # Gera assento aleatório (ex: 12A, 5C)
            fileira = random.randint(1, 30)
            letra = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
            reserva['Assentos'][voo] = f"{fileira}{letra}"
    
    reserva['Status_Checkin'] = True
    salvar_reservas(reservas)

    # 5. Prepara dados para o Cartão de Embarque
    dados_voos = []
    for codigo_voo in reserva['Voos']:
        if codigo_voo in voos:
            v = voos[codigo_voo]
            dados_voos.append({
                'codigo': codigo_voo,
                'origem': v['Origem'],
                'destino': v['Destino'],
                'data': v.get('Datas', ['TBD'])[0],
                'horario': "14:30", # Simulado
                'portao': random.randint(1, 15), # Simulado
                'assento': reserva['Assentos'].get(codigo_voo, '??'),
                'aeronave': v['Aeronave']
            })

    return render_template('passageiros/cartao_embarque.html', reserva=reserva, voos=dados_voos, codigo=codigo_reserva)

if __name__ == '__main__':
    app.run(debug=True)