from flask import Flask, render_template

app = Flask(__name__, template_folder="modulos")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/ventas")
def ventas():
    return render_template("ventas/ventas.html")


@app.route("/produccion")
def produccion():
    return render_template("produccion/produccion.html")

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores/proveedores.html")

if __name__ == "__main__":
    app.run(port=7000, debug=True)