
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from models import db, Receta, MateriaPrima, RecetaIngrediente, Producto
from datetime import datetime

import os
from werkzeug.utils import secure_filename
from decimal import Decimal, ROUND_HALF_UP
from utils import role_required
import forms
from flask_login import login_required

recetas = Blueprint('recetas', __name__, template_folder='../../templates/recetas')

@recetas.route("/nuevaReceta", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def nuevaReceta(): 
    form = forms.RecetaForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        session['receta'] = {
            'nombre': form.nombre.data,
            'cantidad_produccion': form.cantidad_produccion.data,
            'peso': form.peso.data
        }
        return redirect(url_for('recetas.agregarIngredientes'))

    return render_template("recetas/nuevaReceta.html", form=form)

@recetas.route("/nuevaRecetaIngredientes", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def agregarIngredientes():
    form = forms.RecetaIngredientesForm()
    
    ingredientes = MateriaPrima.query.all()
    form.ingrediente.choices = [(str(i.idIngrediente), f"{i.nombre} ({i.tipo})") for i in ingredientes]

    if 'ingredientes' not in session:
        session['ingredientes'] = []

    if request.method == 'POST' and form.validate_on_submit():
        ingrediente_id = form.ingrediente.data
        cantidad = form.cantidad.data
        
        ingrediente_obj = MateriaPrima.query.get(int(ingrediente_id))
        if ingrediente_obj:
            ingrediente_info = {
                'id': ingrediente_obj.idIngrediente,
                'nombre': ingrediente_obj.nombre,
                'tipo': ingrediente_obj.tipo,
                'cantidad': cantidad
            }
            
            ingredientes_session = session['ingredientes']
            ingredientes_session.append(ingrediente_info)
            session['ingredientes'] = ingredientes_session
            flash(f'Ingrediente agregado.', 'success')
            return redirect(url_for('recetas.agregarIngredientes'))

    return render_template("recetas/nuevaRecetaIngredientes.html", form=form)

@recetas.route("/agregarFoto", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def agregarFoto():
    form = forms.RecetaImagenForm()

    if request.method == 'POST' and form.validate_on_submit():
        imagen = form.imagen.data

        if imagen:            
            filename = secure_filename(imagen.filename)
            ruta = os.path.join(current_app.root_path, 'static/imagenes_productos', filename)
            imagen.save(ruta)
            
            session['imagen_producto'] = filename            
            return redirect(url_for('recetas.finalizar')) 

    return render_template("recetas/agregarFoto.html", form=form)

@recetas.route("/cancelarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def cancelar():
    session.pop('receta', None)
    session.pop('ingredientes', None)
    session.pop('imagen_producto', None)
    flash("Operación cancelada.", "warning")    
    return redirect(url_for('recetas.nuevaReceta'))

@recetas.route("/finalizar", methods=['GET'])
@login_required
@role_required('Cocinero', 'Administrador')
def finalizar():
    try:
        # Validación de datos requeridos
        if not all(key in session for key in ['receta', 'ingredientes', 'imagen_producto']):
            flash('Faltan datos para completar la receta.', 'danger')
            return redirect(url_for('recetas.nuevaReceta'))

        datos_receta = session['receta']
        ingredientes = session['ingredientes']
        imagen = session['imagen_producto']

        # Validación de datos básicos
        required_fields = ['nombre', 'cantidad_produccion', 'peso']
        if not all(field in datos_receta for field in required_fields):
            flash('Datos de la receta incompletos.', 'danger')
            return redirect(url_for('recetas.nuevaReceta'))

        # Convertir y validar valores numéricos
        try:
            peso_gramos = Decimal(str(datos_receta['peso']))
            cantidad_piezas = int(datos_receta['cantidad_produccion'])
            
            if peso_gramos <= 0 or cantidad_piezas <= 0:
                flash('El peso y la cantidad deben ser valores positivos.', 'danger')
                return redirect(url_for('recetas.nuevaReceta'))
        except (ValueError, TypeError):
            flash('Valores numéricos inválidos.', 'danger')
            return redirect(url_for('recetas.nuevaReceta'))

        # Crear la receta principal
        nueva_receta = Receta(
            nombre=datos_receta['nombre'],
            cantidad_produccion=cantidad_piezas,
            precioProduccion=Decimal('0.00')
        )
        db.session.add(nueva_receta)
        db.session.flush()

        # Calcular costos y agregar ingredientes
        total_costo = Decimal('0.00')
        
        for item in ingredientes:
            ingrediente = MateriaPrima.query.get(item['id'])
            if not ingrediente:
                flash(f'Ingrediente con ID {item["id"]} no encontrado.', 'warning')
                continue

            try:
                cantidad_ingrediente = Decimal(str(item['cantidad']))
                if ingrediente.cantidad_original and ingrediente.precio_unitario:
                    proporcion = cantidad_ingrediente / Decimal(ingrediente.cantidad_original)
                    costo = proporcion * Decimal(ingrediente.precio_unitario)
                    total_costo += costo

                # Registrar ingrediente en la receta
                detalle = RecetaIngrediente(
                    idReceta=nueva_receta.idReceta,
                    idIngrediente=item['id'],
                    cantidad=cantidad_ingrediente
                )
                db.session.add(detalle)
            except (ValueError, TypeError):
                flash(f'Error en cantidad del ingrediente {item.get("nombre", "")}', 'warning')
                continue

        # Actualizar costo total de producción
        nueva_receta.precioProduccion = total_costo
        db.session.flush()

        # Calcular pesos y precios unitarios
        peso_unitario_gramos = peso_gramos / Decimal(cantidad_piezas)
        precio_unitario_pieza = total_costo / Decimal(cantidad_piezas)
        precio_unitario_gramo = total_costo / peso_gramos

        # Configuración de tipos de productos finales
        tipos_productos = [
            {
                'tipo': 'Piezas',
                'peso': peso_unitario_gramos,
                'margen': Decimal('1.35'),  # 35% de ganancia
                'descripcion': 'Piezas individuales'
            },
            {
                'tipo': 'Pre-empacada 700 gr',
                'peso': Decimal('700'),
                'margen': Decimal('1.30'),  # 30% de ganancia
                'descripcion': 'Paquete de 700 gramos'
            },
            {
                'tipo': 'Pre-empacada 1Kg',
                'peso': Decimal('1000'),
                'margen': Decimal('1.30'),  # 30% de ganancia
                'descripcion': 'Paquete de 1 kilogramo'
            }
        ]

        # Crear los productos finales
        for producto_info in tipos_productos:
            if producto_info['tipo'] == 'Piezas':
                precio_base = precio_unitario_pieza
            else:
                precio_base = precio_unitario_gramo * producto_info['peso']

            precio_final = (precio_base * producto_info['margen']).quantize(
                Decimal('0.01'), 
                rounding=ROUND_HALF_UP
            )

            producto = Producto(
                nombre=nueva_receta.nombre,
                tipo=producto_info['tipo'],
                precio=precio_final,
                cantidad_stock=0,
                fecha_caducidad=None,
                peso=float(producto_info['peso']),  # Convertir a float para la DB
                fecha_produccion=datetime.utcnow(),
                imagen=imagen
            )
            db.session.add(producto)

        # Confirmar todos los cambios en la base de datos
        db.session.commit()

        # Limpiar la sesión
        session.pop('receta', None)
        session.pop('ingredientes', None)
        session.pop('imagen_producto', None)

        flash('Receta y productos creados exitosamente.', 'success')
        return redirect(url_for('recetas.nuevaReceta'))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al guardar la receta: {str(e)}', exc_info=True)
        flash(f'Error al guardar la receta: {str(e)}', 'danger')
        return redirect(url_for('recetas.nuevaReceta'))