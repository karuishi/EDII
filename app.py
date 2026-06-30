import os
from flask import Flask, render_template
from src.database import voos
from src.routes.auth import auth_bp
from src.routes.passageiro import passageiro_bp
from src.routes.admin import admin_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_ed2')

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