from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

recetas = Blueprint('recetas', __name__)

@recetas.route("/CRUDrecetas", methods=['GET', 'POST'])
# cuando este terminado el login y no se necesiten hacer pruebas poner ->@login_required
def funcion():
    
    return render_template("recetas/CRUDrecetas.html")