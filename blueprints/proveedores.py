from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

proveedores = Blueprint('proveedores', __name__)

@proveedores.route("/CRUDproveedores", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def funcion():
    
    return render_template("proveedores/CRUDproveedores.html")

@proveedores.route("/ordenar", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def ordenar():
    
    return render_template("proveedores/ordenar.html")