from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.database import voos, dados_clientes, reservas, clientes_btree_cpf
from src.models.data_manager import salvar_voos, salvar_clientes, salvar_reservas, gerar_codigo_reserva

admin_bp = Blueprint('admin', __name__)

# --- VOOS ---
@admin_bp.route('/voos')
def listar_voos():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    return render_template('voos/voos.html', voos=voos)

@admin_bp.route('/voos/adicionar', methods=['GET', 'POST'])
def adicionar_voo():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
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
        return redirect(url_for('admin.listar_voos'))
    return render_template('voos/adicionar_voo.html')

@admin_bp.route('/voos/editar/<codigo_voo>', methods=['GET', 'POST'])
def editar_voo(codigo_voo):
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    voo = voos.get(codigo_voo)
    if request.method == 'POST':
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
        return redirect(url_for('admin.listar_voos'))
    return render_template('voos/editar_voo.html', voo=voo, codigo_voo=codigo_voo)

@admin_bp.route('/voos/excluir/<codigo_voo>')
def excluir_voo(codigo_voo):
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    for res in reservas.values():
        if codigo_voo in res['Voos']:
            flash(f'Não é possível excluir o voo {codigo_voo} pois existem reservas associadas.', 'danger')
            return redirect(url_for('admin.listar_voos'))
    
    if codigo_voo in voos:
        del voos[codigo_voo]
        salvar_voos(voos)
        flash('Voo excluído com sucesso.', 'success')
    return redirect(url_for('admin.listar_voos'))

# --- CLIENTES ---
@admin_bp.route('/clientes')
def listar_clientes():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
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

@admin_bp.route('/clientes/adicionar', methods=['GET', 'POST'])
def adicionar_cliente():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    if request.method == 'POST':
        try:
            cpf = int(request.form['cpf'])
        except ValueError:
            return "Erro: CPF deve conter apenas números."

        if clientes_btree_cpf.buscar(cpf):
            return "Erro: Cliente com este CPF já cadastrado!"
        
        nome = request.form['nome']
        clientes_btree_cpf.inserir(cpf)
        dados_clientes[cpf] = {
            "Nome" : nome,
            "Reservas" : [],
            "Data_viagem" : request.form['data_viagem'],
            "Milhas" : request.form['milhas']
        }
        salvar_clientes(dados_clientes)
        return redirect(url_for('admin.listar_clientes'))
    return render_template('clientes/adicionar_cliente.html')

@admin_bp.route('/clientes/ordenar_cpf')
def listar_clientes_cpf():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    cpfs_ordenados = clientes_btree_cpf.listar_cpfs()
    lista_final = []
    for cpf in cpfs_ordenados:
        if cpf in dados_clientes:
            lista_final.append((cpf, dados_clientes[cpf]))
    return render_template('clientes/clientes.html', clientes_ordenados=lista_final)

# --- RESERVAS ---
@admin_bp.route('/reservas')
def listar_reservas():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    return render_template('reservas/reservas.html', reservas=reservas)

@admin_bp.route('/reservas/nova', methods=['GET', 'POST'])
def fazer_reserva():
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    if request.method == 'GET':
        return render_template('reservas/adicionar_reserva.html', voos=voos, clientes=dados_clientes)

    if request.method == 'POST':
        try:
            cpf_cliente = int(request.form['cpf_cliente'])
        except ValueError:
            flash("Erro: CPF inválido.", 'danger')
            return redirect(url_for('admin.fazer_reserva'))

        voos_selecionados = request.form.getlist('voos_selecionados')

        if not voos_selecionados:
            flash("Nenhum voo selecionado.", 'danger')
            return redirect(url_for('admin.fazer_reserva'))

        for codigo_voo in voos_selecionados:
            if voos[codigo_voo]['Total_assentos'] <= 0:
                flash(f'Voo {codigo_voo} esgotado!', 'danger')
                return redirect(url_for('admin.fazer_reserva'))
        
        total_milhas_novas = 0
        proxima_data_encontrada = ""

        for codigo_voo in voos_selecionados:
            voos[codigo_voo]['Total_assentos'] -= 1
            total_milhas_novas += voos[codigo_voo]['Milhas']
            if not proxima_data_encontrada:
                datas = voos[codigo_voo].get('Datas', [])
                if datas: proxima_data_encontrada = datas[0]
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

        flash(f'Reserva {novo_codigo} realizada com sucesso!', 'success')
        return redirect(url_for('admin.fazer_reserva'))

@admin_bp.route('/reservas/detalhes/<codigo_reserva>')
def detalhes_reserva(codigo_reserva):
    reserva = reservas.get(codigo_reserva)
    if not reserva:
        flash('Reserva não encontrada.', 'danger')
        return redirect(url_for('admin.listar_reservas'))

    eh_admin = session.get('role') == 'admin'
    cpf_usuario = session.get('cpf')
    eh_dono = cpf_usuario and int(cpf_usuario) == int(reserva['CPF'])

    if not (eh_admin or eh_dono):
        flash('Acesso negado.', 'danger')
        return redirect(url_for('passageiro.pagina_passageiro'))
    
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
                           reserva=reserva, codigo=codigo_reserva, voos=detalhes_voos, 
                           total_preco=total_preco, total_milhas=total_milhas)

@admin_bp.route('/reservas/excluir/<codigo_reserva>')
def excluir_reserva(codigo_reserva):
    if session.get('role') != 'admin':
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    reserva = reservas.get(codigo_reserva)
    if not reserva:
        flash('Reserva não encontrada.', 'danger')
        return redirect(url_for('admin.listar_reservas'))
    
    cpf_cliente = int(reserva['CPF'])
    voos_reserva = reserva['Voos']
    
    # Devolve assentos e remove milhas
    milhas_a_remover = 0
    for codigo_voo in voos_reserva:
        if codigo_voo in voos:
            voos[codigo_voo]['Total_assentos'] += 1
            milhas_a_remover += voos[codigo_voo]['Milhas']
    salvar_voos(voos)
    
    if cpf_cliente in dados_clientes:
        cliente = dados_clientes[cpf_cliente]
        if codigo_reserva in cliente['Reservas']:
            cliente['Reservas'].remove(codigo_reserva)
        milhas_atuais = int(cliente.get('Milhas', 0))
        cliente['Milhas'] = max(0, milhas_atuais - milhas_a_remover)
        salvar_clientes(dados_clientes)
        
    del reservas[codigo_reserva]
    salvar_reservas(reservas)
    flash(f'Reserva {codigo_reserva} cancelada com sucesso.', 'success')
    return redirect(url_for('admin.listar_reservas'))