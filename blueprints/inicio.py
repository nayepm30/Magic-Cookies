from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

inicio = Blueprint('inicio', __name__)

@inicio.route("/inicio", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def inici():
    
    return render_template("inicio.html")

@inicio.route("/dashboard", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def dashboard():
    
    return render_template("dashboard.html")