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
    app.run(host="0.0.0.0", port=50000, debug=False)