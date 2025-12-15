from flask import Flask, render_template
from database import voos # Importamos voos apenas para a tela inicial

# Importar os Blueprints (módulos)
from routes.auth import auth_bp
from routes.passageiro import passageiro_bp
from routes.admin import admin_bp

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'chave_secreta_ed2'

# Registar os Blueprints no app principal
app.register_blueprint(auth_bp)
app.register_blueprint(passageiro_bp)
app.register_blueprint(admin_bp)

# Rota Principal (Tela Inicial)
@app.route('/')
def home():
    return render_template('tela_inicial/home.html', voos=voos)

if __name__ == '__main__':
    app.run(debug=True)