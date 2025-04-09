from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required, current_user
from models import *
from decimal import Decimal
from datetime import date
import forms
from utils import role_required

mermas = Blueprint('mermas', __name__)

@mermas.route("/productos", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor', 'Cocinero', 'Administrador')
def mermaProductos():
    create_form = forms.NuevaMerma(request.form)

    productos = db.session.query(Producto.idProducto, Producto.nombre, Producto.tipo, Producto.cantidad_stock).all()
    create_form.materia.choices = [(p.idProducto, f"{p.nombre} - {p.tipo}") for p in productos]
    
    if request.method == 'POST' and create_form.validate(): 
        tipo = "Productos"
        id_producto = create_form.materia.data  
        cantidad = create_form.cantidad.data
        motivo = create_form.motivo.data
        fecha = date.today()
        
        producto = db.session.query(Producto).filter(Producto.idProducto == id_producto).first()
        
        if producto:
            if producto.cantidad_stock >= cantidad:             
                producto.cantidad_stock -= cantidad
                
                nueva_merma = Merma(tipo=tipo, cantidad=cantidad, motivo=motivo, fecha=fecha, idProducto=id_producto)
                db.session.add(nueva_merma)
                db.session.commit()

                flash('Merma registrada, producto restado', 'success')
            else:
                flash('La merma supera el stock disponible', 'danger')
        else:
            flash('Producto no encontrado', 'danger')

        return redirect(url_for('mermas.mermaProductos'))

    return render_template("mermas/mermasProductos.html", form=create_form)

@mermas.route("/insumos", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def mermaInsumos():
    create_form = forms.NuevaMerma(request.form)

    ingredientes = db.session.query(MateriaPrima.idIngrediente, MateriaPrima.nombre, MateriaPrima.tipo, MateriaPrima.cantidad).all()
    create_form.materia.choices = [(i.idIngrediente, f"{i.nombre} - {i.tipo}") for i in ingredientes]

    if request.method == 'POST' and create_form.validate():
        tipo = "Insumos"
        id_ingrediente = create_form.materia.data  
        cantidad = create_form.cantidad.data
        motivo = create_form.motivo.data
        fecha = date.today()

        ingrediente = db.session.query(MateriaPrima).filter(MateriaPrima.idIngrediente == id_ingrediente).first()

        if ingrediente:
            if ingrediente.cantidad >= cantidad:
                ingrediente.cantidad -= cantidad
                
                nueva_merma = Merma(tipo=tipo, cantidad=cantidad, motivo=motivo, fecha=fecha,idIngrediente=id_ingrediente)
                db.session.add(nueva_merma)
                db.session.commit()

                flash('Merma registrada, materia prima restada', 'success')
            else:
                flash('La merma supera el stock disponible de materia prima', 'danger')
        else:
            flash('Materia prima no encontrada', 'danger')

        return redirect(url_for('mermas.mermaInsumos'))

    return render_template("mermas/mermasInsumos.html", form=create_form)

@mermas.route("/historial", methods=['GET'])
@login_required
@role_required('Vendedor', 'Cocinero', 'Administrador')
def historial():
    mermas_detalles = []

    mermas = Merma.query.order_by(Merma.idMerma.desc()).all()

    for merma in mermas:
        detalle_merma = {
            'merma': merma,
            'producto': Producto.query.get(merma.idProducto) if merma.idProducto else None,
            'ingrediente': MateriaPrima.query.get(merma.idIngrediente) if merma.idIngrediente else None
        }
        
        mermas_detalles.append(detalle_merma)

    return render_template('mermas/mermasHistorial.html', mermas_detalles=mermas_detalles)