from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Proveedor 

import forms


proveedores = Blueprint('proveedores', __name__) 

@proveedores.route("/CRUDproveedores", methods=['GET', 'POST'])
#@login_required
def funcion():
    # Obtener todos los proveedores para mostrar en la tabla
    proveedores_lista = Proveedor.query.all()
    return render_template("proveedores/CRUDproveedores.html", proveedores=proveedores_lista)


@proveedores.route('/add_proveedor', methods=['POST'])
def add_proveedor():
    try:
        # Obtener datos del formulario
        nombre = request.form['empresa']
        telefono = request.form['tel']
        producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        presentacion = request.form['presentacion']
        costo = float(request.form['costo'])
        
        # Validaciones básicas
        if not nombre or not producto:
            flash("Nombre de empresa y producto son requeridos", "error")
            return redirect(url_for('proveedores.funcion'))
        
        
        nuevo_proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            direccion="",  # Campo opcional según tu formulario
            Producto=producto,
            Cantidad=cantidad,
            Presentacion=presentacion,  # Añadido para coincidir con tu formulario
            Costo=costo  # Añadido para coincidir con tu formulario
        )
        
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash("Proveedor agregado exitosamente", "success")
        
    except KeyError as e:
        flash(f"Falta campo requerido: {str(e)}", "error")
    except ValueError as e:
        flash(f"Error en formato de datos: {str(e)}", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar: {str(e)}", "error")
    
    return redirect(url_for('proveedores.funcion'))  

@proveedores.route("/ordenar", methods=['GET', 'POST'])
#@login_required
def ordenar():
    return render_template("proveedores/ordenar.html")