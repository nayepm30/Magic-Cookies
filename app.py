from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(port=7000, debug=True)