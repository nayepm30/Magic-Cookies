from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/inicio")
def inicio():
    return render_template("iniciooo.html")

@app.route("/ventas")
def ventas():
    return render_template("ventas.html")

if __name__ == "__main__":
    app.run(debug=True)