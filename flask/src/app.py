from flask import Flask, render_template, request, redirect, url_for
from BTree import BTree
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
            return redirect(url_for('listar_clientes')) # listar_voos
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

# Nome do arquivo onde salvaremos os clientes
ARQUIVO_CLIENTES = 'clientes.json'

def salvar_clientes(dados_clientes):
    with open(ARQUIVO_CLIENTES, 'w') as f:
        # Temos de guardar as chaves (CPFs) como strings no JSON
        dados_para_salvar = {str(cpf): dados for cpf, dados in dados_clientes.items()}
        json.dump(dados_para_salvar, f, indent=4)

def carregar_clientes():
    dados_clientes = {}
    clientes_btree = BTree(t=3) # Cria uma nova Árvore B vazia

    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, 'r') as f:
            dados_do_json = json.load(f)
            
            # Reconstrói o dicionário com chaves INT
            dados_clientes = {int(cpf): dados for cpf, dados in dados_do_json.items()}

            # A "magia" está aqui:
            # Reconstrói o índice da Árvore B a partir dos dados carregados
            print("A reconstruir o índice da Árvore B...")
            for cpf in dados_clientes.keys():
                clientes_btree.insert(cpf)
            print("Índice B-Tree pronto.")
            
    return dados_clientes, clientes_btree

dados_clientes, clientes_btree_cpf = carregar_clientes()

@app.route('/clientes')
def listar_clientes():
    if not dados_clientes:
        return render_template('clientes.html', clientes_ordenados=[])
        
    # Ordena por nome para a exibição principal
    lista_ordenada = sorted(dados_clientes.items(), key=lambda item: item[1]["Nome"])
    
    return render_template('clientes.html', clientes_ordenados=lista_ordenada)

@app.route('/clientes/adicionar', methods=['GET', 'POST'])
def adicionar_cliente():
    if request.method == 'POST':
        try:
            cpf = int(request.form['cpf'])
        except ValueError:
            return "Erro: CPF deve conter apenas números."

        # 1. Verifica na Árvore B (Otimizado!)
        if clientes_btree_cpf.search(cpf):
            return "Erro: Cliente com este CPF já cadastrado!"
        
        # 2. Se não existe, adiciona em ambos
        nome = request.form['nome']
        
        # A. Adiciona ao índice B-Tree
        clientes_btree_cpf.insert(cpf)
        
        # B. Adiciona ao dicionário de dados
        dados_clientes[cpf] = {
            "Nome" : nome,
            "Reservas" : [],
            "Data_viagem" : request.form['data_viagem'],
            "Milhas" : request.form['milhas']
        }
        
        # 3. Salva os dados no ficheiro JSON
        salvar_clientes(dados_clientes)
        
        return redirect(url_for('listar_clientes'))

    # Se for GET, apenas mostra o formulário
    return render_template('adicionar_cliente.html')

@app.route('/clientes/ordenar_cpf')
def listar_clientes_cpf():
    if not dados_clientes:
        return render_template('clientes.html', clientes_ordenados=[])
        
    # Pega todos os CPFs (keys), que a B-Tree otimizaria
    cpfs_ordenados = sorted(dados_clientes.keys())
    
    # Monta a lista ordenada para o template
    lista_final = []
    for cpf in cpfs_ordenados:
        lista_final.append( (cpf, dados_clientes[cpf]) )
        
    return render_template('clientes.html', clientes_ordenados=lista_final)
if __name__ == '__main__':
    app.run(debug=True)