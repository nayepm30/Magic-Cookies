from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import Receta, RecetaIngrediente, MateriaPrima, Producto, db
from datetime import timedelta, datetime
from utils import role_required
from flask_login import login_required


produccion = Blueprint('produccion', __name__)

@produccion.route("/produccion", methods=['GET'])
@login_required
@role_required('Cocinero', 'Administrador')
def recetas():
    recetas = Receta.query.all()    
    recetasYproductos = []
    for receta in recetas:
        producto = Producto.query.filter_by(nombre=receta.nombre, tipo='Piezas').first()
        recetasYproductos.append({
            'receta': receta,
            'producto': producto
        })
    return render_template("produccion/produccion.html", recetas=recetasYproductos)

@produccion.route("/detalles", methods=['POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def detalles():
    id_receta = request.form.get("idReceta")
    receta = Receta.query.get(id_receta)

    ingredientes_detalle = []
    for ri in receta.receta_ingredientes:
        ingrediente = MateriaPrima.query.get(ri.idIngrediente)
        ingredientes_detalle.append({
            'nombre': ingrediente.nombre,
            'cantidad_necesaria': ri.cantidad,
            'stock_disponible': ingrediente.cantidad
        })

    return render_template("produccion/detalles.html", receta=receta, ingredientes=ingredientes_detalle)


@produccion.route("/realizar", methods=['POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def producir():
    from datetime import datetime, timedelta

    id_receta = request.form.get("idReceta")
    receta = Receta.query.get(id_receta)

    for ri in receta.receta_ingredientes:
        ingrediente = MateriaPrima.query.get(ri.idIngrediente)
        if ingrediente.cantidad < ri.cantidad:
            flash(f"No hay suficiente stock de {ingrediente.nombre}.", "error")
            return redirect(url_for("produccion.recetas"))
    
    for ri in receta.receta_ingredientes:
        ingrediente = MateriaPrima.query.get(ri.idIngrediente)
        ingrediente.cantidad -= ri.cantidad
        db.session.add(ingrediente)
    
    producto = Producto.query.filter_by(nombre=receta.nombre, tipo='Piezas').first()

    if producto:
        producto.cantidad_stock += receta.cantidad_produccion
        producto.fecha_produccion = datetime.now()
        producto.fecha_caducidad = datetime.now() + timedelta(days=7)
        db.session.add(producto)
    else:
        flash("No se encontró un producto asociado de tipo 'Piezas'.", "error")
        return redirect(url_for("produccion.recetas"))

    db.session.commit()
    flash("Producción realizada correctamente.", "success")
    return redirect(url_for("produccion.recetas"))