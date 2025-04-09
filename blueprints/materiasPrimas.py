from flask import Blueprint, render_template
from models import MateriaPrima, Proveedor, db
import datetime
from flask_login import login_required
from utils import role_required

materia = Blueprint('materia', __name__)

@materia.route("/materiasPrimas", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def funcion():
    materias_primas = db.session.query(MateriaPrima, Proveedor).join(Proveedor, MateriaPrima.idProveedores == Proveedor.idProveedores).all()

    return render_template("materiasPrimas/materiasPrimas.html",materias_primas=materias_primas,datetime=datetime)  