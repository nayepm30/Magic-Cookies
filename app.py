from flask import Flask, render_template
from flask_login import LoginManager
from models import db, Usuario
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_mail import Mail

from blueprints.auth import auth
from blueprints.inicio import inicio
from blueprints.carrito import carrito
from blueprints.materiasPrimas import materia
from blueprints.produccion import produccion
from blueprints.proveedores import proveedores
from blueprints.recetas import recetas
from blueprints.ventas import ventas
from blueprints.mermas import mermas
from blueprints.usuarios import usuarios

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
db.init_app(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(inicio, url_prefix='/inicio')
app.register_blueprint(carrito, url_prefix='/carrito')
app.register_blueprint(materia, url_prefix='/materia')
app.register_blueprint(produccion, url_prefix='/produccion') #
app.register_blueprint(proveedores, url_prefix='/proveedores')
app.register_blueprint(recetas, url_prefix='/recetas')
app.register_blueprint(ventas, url_prefix='/ventas')
app.register_blueprint(mermas, url_prefix='/mermas')
app.register_blueprint(usuarios, url_prefix='/usuarios')

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)