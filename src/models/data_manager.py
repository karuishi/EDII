import json
import os
from .BTree import BTree

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

ARQUIVO_VOOS = os.path.join(DATA_DIR, 'voos.json')
ARQUIVO_CLIENTES = os.path.join(DATA_DIR, 'clientes.json')
ARQUIVO_RESERVAS = os.path.join(DATA_DIR, 'reservas.json')
ARQUIVO_LOGIN = os.path.join(DATA_DIR, 'login.json')

# --- Funções de Login ---
def carregar_login():
    if os.path.exists(ARQUIVO_LOGIN):
        with open(ARQUIVO_LOGIN, 'r') as f:
            return json.load(f)
    # Retorna um dict de exemplo se o ficheiro não existir
    return { "Admin": { "senha": "admin", "role": "admin" } } 

def salvar_login(login):
    with open(ARQUIVO_LOGIN, 'w') as f:
        json.dump(login, f, indent=4)

# --- Funções de Voos ---
def carregar_voos():
    if os.path.exists(ARQUIVO_VOOS):
        with open(ARQUIVO_VOOS, 'r') as f:
            return json.load(f)
    return {} # Retorna vazio se não existir

def salvar_voos(voos):
    with open(ARQUIVO_VOOS, 'w') as f:
        json.dump(voos, f, indent=4)

# --- Funções de Clientes ---
def carregar_clientes():
    dados_clientes = {}
    clientes_btree = BTree(grau_min=3) 

    if os.path.exists(ARQUIVO_CLIENTES):
        try:
            with open(ARQUIVO_CLIENTES, 'r') as f:
                dados_do_json = json.load(f)
            
            dados_clientes = {int(cpf): dados for cpf, dados in dados_do_json.items()}

            print("A reconstruir o índice da Árvore B...")
            for cpf in dados_clientes.keys():
                clientes_btree.inserir(cpf)
            print("Índice B-Tree pronto.")
        
        except json.JSONDecodeError:
            print(f"Aviso: {ARQUIVO_CLIENTES} está vazio ou corrompido. A começar do zero.")
            
    return dados_clientes, clientes_btree

def salvar_clientes(dados_clientes):
    with open(ARQUIVO_CLIENTES, 'w') as f:
        dados_para_salvar = {str(cpf): dados for cpf, dados in dados_clientes.items()}
        json.dump(dados_para_salvar, f, indent=4)

# --- Funções de Reservas ---
def carregar_reservas():
    if os.path.exists(ARQUIVO_RESERVAS):
        try:
            with open(ARQUIVO_RESERVAS, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} 
    return {}

def salvar_reservas(reservas):
    with open(ARQUIVO_RESERVAS, 'w') as f:
        json.dump(reservas, f, indent=4)

def gerar_codigo_reserva(reservas):
    if not reservas:
        return "RES1"
    
    numeros = [int(cod.replace('RES', '')) for cod in reservas.keys()]
    prox_codigo = max(numeros) + 1
    return f"RES{prox_codigo}"