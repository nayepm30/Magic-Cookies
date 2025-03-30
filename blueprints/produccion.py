from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

produccion = Blueprint('produccion', __name__)

@produccion.route("/produccion", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def funcion():
    
    return render_template("produccion/produccion.html")

