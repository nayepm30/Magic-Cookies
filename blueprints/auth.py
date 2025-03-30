from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import *
import forms

auth = Blueprint('auth', __name__)


@auth.route("/", methods=['GET', 'POST'])
def login():
    create_form = forms.inicioSesion(request.form)

    if request.method == 'POST' and create_form.validate():
        usu = create_form.username.data.strip()
        pas = create_form.password.data.strip()

        sesion = Usuario.query.filter_by(username=usu, password=pas).first()

        if sesion:
            login_user(sesion)            
            flash("Inicio de sesión.", "success")
            return redirect(url_for('auth.inicio'))
        else:                         
                flash("Usuario o contraseña incorrectos.", "danger")
                return redirect(url_for('auth.inicio'))

    return render_template("login.html", form=create_form)

@auth.route("/logout")
@login_required
def logout():    
    logout_user()
    flash("Fin de sesión.", "info")
    return redirect(url_for('auth.login'))
