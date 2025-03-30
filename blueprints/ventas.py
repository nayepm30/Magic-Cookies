from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

ventas = Blueprint('ventas', __name__)

@ventas.route("/registrar", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def registrar():
    
    return render_template("ventas/registrar.html")

@ventas.route("/corte", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def corte():
    
    return render_template("ventas/corte.html")

@ventas.route("/historial", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def historial():
    
    return render_template("ventas/historial.html")

@ventas.route("/pedidos", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def pedidos():
    
    return render_template("ventas/pedidos.html")