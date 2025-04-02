from flask import Flask, render_template
from blueprints.proveedores import proveedores 
from blueprints.carrito import carrito 
import os



app = Flask(__name__)

app.register_blueprint(proveedores, url_prefix='/proveedores')

app.register_blueprint(carrito, url_prefix='/carrito')

app.secret_key = os.urandom(24).hex()  # Genera una clave aleatoria

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/registrar")
def ventas():
    return render_template("ventas/registrarVentas.html")

@app.route("/produccion")
def produccion():
    return render_template("produccion/produccion.html")

@app.route("/CRUDproveedores")
def proveedores():
    return render_template("proveedores/CRUDproveedores.html")

@app.route("/ordenar")
def ordenar():
    return render_template("proveedores/ordenar.html")

@app.route("/CRUDrecetas")
def recetas():
    return render_template("recetas/CRUDrecetas.html")

@app.route("/productos")
def invproductos():
    return render_template("inventario/productos.html")

@app.route("/materiasPrimas")
def matPrimas():
    return render_template("materiasPrimas/materiasPrimas.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")

@app.route("/galletas")
def galletas():
    return render_template("galletas.html")


@app.route("/presentaciones")
def presentaciones():
    return render_template("presentaciones.html")

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos.html")

@app.route("/carrito")
def carrito():
    return render_template("carrito.html")

from flask import jsonify, session

@app.route('/check-session')
def check_session():
    # Verifica si el usuario está en la sesión
    # Ajusta esto según cómo manejas las sesiones en tu aplicación
    is_logged_in = 'user_id' in session  # o la clave que uses para almacenar el usuario
    return jsonify({'isLoggedIn': is_logged_in})

if __name__ == "__main__":
    app.run(port=7000, debug=True)