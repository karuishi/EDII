from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.database import voos, reservas, dados_clientes, grafos_voos
from src.models.data_manager import salvar_voos, salvar_reservas, salvar_clientes, gerar_codigo_reserva
from src.models.grafo import GrafoRotas
import folium
import random

passageiro_bp = Blueprint('passageiro', __name__)

@passageiro_bp.route('/passageiro')
def pagina_passageiro():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    role = session.get('role')
    cpf_sessao = session.get('cpf')

    # Busca os dados do cliente para exibir no painel
    dados_do_clientes = {}
    if role == 'admin':
        dados_do_clientes = {"Nome": "ADM", "Milhas": "∞"}
        cpf_atual = 0
    elif cpf_sessao:
        try:
            cpf_atual = int(cpf_sessao)
            dados_do_clientes = dados_clientes.get(cpf_atual, {})
        except ValueError:
            return redirect(url_for('auth.logout'))
    
    origem_filtro = request.args.get('origem')
    destino_filtro = request.args.get('destino')
    data_ida_filtro = request.args.get('data_ida')

    voos_exibicao = {}
    
    # 1. Busca por Voos Diretos
    if origem_filtro or destino_filtro or data_ida_filtro:
        for codigo, dados in voos.items():
            corresponde = True
            if origem_filtro and dados['Origem'].lower() != origem_filtro.lower(): corresponde = False
            if corresponde and destino_filtro and dados['Destino'].lower() != destino_filtro.lower(): corresponde = False
            if corresponde and data_ida_filtro:
                if data_ida_filtro not in dados.get('Datas', []): corresponde = False
            
            if corresponde:
                voos_exibicao[codigo] = dados
    else:
        voos_exibicao = voos.copy()

    # 2. Busca por voos com conexão usando o Grafo
    if origem_filtro and destino_filtro and not voos_exibicao:
        # Recria o Grafo para garantir dados novos
        grafo_atualizado = GrafoRotas()
        for cod, dados in voos.items():
            grafo_atualizado.adicionar_rota(dados['Origem'], dados['Destino'], cod, dados['Preco'])

        resultado_grafo = grafo_atualizado.buscar_melhor_rota(origem_filtro, destino_filtro)
        
        if resultado_grafo:
            custo_total, caminho_codigos = resultado_grafo
            if len(caminho_codigos) > 1:
                # Usa UNDERSCORE para juntar os códigos da conexão em uma string só (exemplo: CONEXAO-ED-001_ED-002)
                codigo_combo = "CONEXAO-" + "_".join(caminho_codigos)
                primeiro_voo = voos[caminho_codigos[0]]
                
                voos_exibicao[codigo_combo] = {
                    "Origem": origem_filtro,
                    "Destino": destino_filtro,
                    "Preco": custo_total,
                    "Aeronave": f"Voo com {len(caminho_codigos)-1} Escala(s)",
                    "Milhas": sum(voos[c]['Milhas'] for c in caminho_codigos),
                    "Datas": primeiro_voo.get('Datas', []),
                    "Total_assentos": min(voos[c]['Total_assentos'] for c in caminho_codigos),
                    "Eh_Conexao": True
                }
                flash(f"Rota com conexão encontrada via {len(caminho_codigos)} voos!", "info")
    
    # Filtra reservas do cliente logado
    minhas_reservas = {}
    if role != 'admin' and cpf_sessao:
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

@passageiro_bp.route('/passageiro/reservar/<codigo_voo>')
def reservar_passagem(codigo_voo):
    if 'usuario' not in session: return redirect(url_for('auth.login'))
    if session.get('role') == 'admin': return redirect(url_for('passageiro.pagina_passageiro'))
    
    cpf_sessao = session.get('cpf')
    if not cpf_sessao:
        flash('CPF não encontrado na sessão. Faça login novamente.', 'danger')
        return redirect(url_for('auth.logout'))
    cpf_cliente = int(cpf_sessao)
    lista_voos_para_reservar = []
    
    # Se for uma conexão, divide a string para pegar a lista de voos individuais
    if codigo_voo.startswith("CONEXAO-"):
        trecho_codigos = codigo_voo.replace("CONEXAO-", "")
        lista_voos_para_reservar = trecho_codigos.split("_")
    else:
        lista_voos_para_reservar = [codigo_voo]

    total_milhas_ganhas = 0
    primeira_data = ""

    # Validações
    for cod in lista_voos_para_reservar:
        if cod not in voos:
            flash(f"Erro: O voo '{cod}' não está disponível.", 'danger')
            return redirect(url_for('passageiro.pagina_passageiro'))
        if voos[cod]['Total_assentos'] <= 0:
            flash(f"O voo {cod} está lotado!", 'danger')
            return redirect(url_for('passageiro.pagina_passageiro'))
        
        total_milhas_ganhas += voos[cod]['Milhas']
        if not primeira_data:
            datas = voos[cod].get('Datas', [])
            if datas: primeira_data = datas[0]

    # Debita Assentos
    for cod in lista_voos_para_reservar:
        voos[cod]['Total_assentos'] -= 1
    salvar_voos(voos)

    # Cria Reserva
    novo_codigo_reserva = gerar_codigo_reserva(reservas)
    reservas[novo_codigo_reserva] = {
        "Cliente": dados_clientes[cpf_cliente]['Nome'],
        "CPF": cpf_cliente,
        "Voos": lista_voos_para_reservar
    }
    salvar_reservas(reservas)

    # Atualiza Cliente
    dados_clientes[cpf_cliente]['Reservas'].append(novo_codigo_reserva)
    milhas_atuais = int(dados_clientes[cpf_cliente].get('Milhas', 0))
    dados_clientes[cpf_cliente]['Milhas'] = milhas_atuais + total_milhas_ganhas
    
    if primeira_data:
        dados_clientes[cpf_cliente]['Data_viagem'] = primeira_data

    salvar_clientes(dados_clientes)

    flash(f'Reserva {novo_codigo_reserva} realizada com sucesso!', 'success')
    return redirect(url_for('passageiro.pagina_passageiro'))

@passageiro_bp.route('/checkin', methods=['POST'])
def realizar_checkin():
    codigo_reserva = request.form.get('codigo_reserva')
    
    if not codigo_reserva:
        flash('Por favor, digite o código da reserva.', 'warning')
        return redirect(url_for('passageiro.pagina_passageiro'))
    
    codigo_reserva = codigo_reserva.upper()
    reserva = reservas.get(codigo_reserva)
    
    if not reserva:
        flash(f'Reserva {codigo_reserva} não encontrada.', 'danger')
        return redirect(url_for('passageiro.pagina_passageiro') + '#checkin')

    if session.get('role') != 'admin':
        cpf_logado = session.get('cpf')
        if not cpf_logado or int(reserva['CPF']) != int(cpf_logado):
             flash('Você só pode fazer check-in das suas próprias reservas.', 'danger')
             return redirect(url_for('passageiro.pagina_passageiro') + '#checkin')

    if 'Assentos' not in reserva:
        reserva['Assentos'] = {}
        for voo in reserva['Voos']:
            fileira = random.randint(1, 30)
            letra = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
            reserva['Assentos'][voo] = f"{fileira}{letra}"
    
    reserva['Status_Checkin'] = True
    salvar_reservas(reservas)

    dados_voos = []
    for codigo_voo in reserva['Voos']:
        if codigo_voo in voos:
            v = voos[codigo_voo]
            dados_voos.append({
                'codigo': codigo_voo,
                'origem': v['Origem'],
                'destino': v['Destino'],
                'data': v.get('Datas', ['TBD'])[0],
                'horario': "14:30",
                'portao': random.randint(1, 15),
                'assento': reserva['Assentos'].get(codigo_voo, '??'),
                'aeronave': v['Aeronave']
            })

    return render_template('passageiros/cartao_embarque.html', reserva=reserva, voos=dados_voos, codigo=codigo_reserva)

@passageiro_bp.route('/mapa')
def mapa_voos():
    theme = request.args.get('theme', 'light')
    
    if theme == 'dark':
        tiles = 'CartoDB dark_matter'
        line_color = '#0d6efd'
        marker_color = '#ffc107'
    else:
        tiles = 'CartoDB positron'
        line_color = '#0d6efd'
        marker_color = '#0d6efd'

    coordenadas = {
        "Salvador": [-12.9704, -38.5124],
        "São Paulo": [-23.5505, -46.6333],
        "Rio de Janeiro": [-22.9068, -43.1729],
        "Brasília": [-15.7801, -47.9292],
        "Belém": [-1.4558, -48.4902],
        "Fortaleza": [-3.7172, -38.5434],
        "Recife": [-8.0476, -34.8770],
        "Curitiba": [-25.4284, -49.2733],
        "Porto Alegre": [-30.0346, -51.2177],
        "Manaus": [-3.1190, -60.0217]
    }

    m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4, tiles=tiles)
    cidades_adicionadas = set()

    for codigo, dados in voos.items():
        origem_nome = dados['Origem'].split(' - ')[0]
        destino_nome = dados['Destino'].split(' - ')[0]
        coord_origem = coordenadas.get(origem_nome)
        coord_destino = coordenadas.get(destino_nome)

        if coord_origem and coord_destino:
            folium.PolyLine(locations=[coord_origem, coord_destino], color=line_color, weight=2, opacity=0.7, tooltip=f"Voo {codigo}").add_to(m)
            for nome, coord in [(origem_nome, coord_origem), (destino_nome, coord_destino)]:
                if nome not in cidades_adicionadas:
                    folium.CircleMarker(location=coord, radius=6, color=marker_color, fill=True, fill_color=marker_color, fill_opacity=1, popup=nome, tooltip=nome).add_to(m)
                    cidades_adicionadas.add(nome)

    return m._repr_html_()