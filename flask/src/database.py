# src/database.py
from data_manager import carregar_voos, carregar_clientes, carregar_reservas, carregar_login
from grafo import GrafoRotas

# Carregamento de dados globais
print("A carregar base de dados...")
voos = carregar_voos()
dados_clientes, clientes_btree_cpf = carregar_clientes()
reservas = carregar_reservas()
login_senha = carregar_login()

# Inicialização do Grafo
grafos_voos = GrafoRotas()
for codigo, dados in voos.items():
    grafos_voos.adicionar_rota(dados['Origem'], dados['Destino'], codigo, dados['Preco'])