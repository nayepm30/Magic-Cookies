
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Proveedor, ProveedorProductos, OrdenProductos, Orden, MateriaPrima
import forms
from datetime import datetime 
from utils import role_required
from flask_login import login_required

proveedores = Blueprint('proveedores', __name__)

@proveedores.route("/nuevoProveedor", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def nuevo(): 
    create_form = forms.ProveedorNuevoForm(request.form)    
    
    if 'infoProveedor' not in session:
        session['infoProveedor'] = []
    
    if request.method == 'POST' and create_form.validate():
        nombre = create_form.nombre.data,
        telefono = create_form.telefono.data,
        direccion = create_form.direccion.data
                
        session['infoProveedor'] = {
                    'nombre': nombre,
                    'telefono': telefono,
                    'direccion': direccion
                }
        session.modified = True 

        flash("Proveedor guardado.", "success")
        
        return redirect(url_for('proveedores.nuevoProductos'))

    return render_template("proveedores/nuevoProveedor.html", form=create_form)

@proveedores.route("/nuevoProveedorProductos", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def nuevoProductos(): 
    create_form = forms.ProveedorProductosForm(request.form)    
    
    if 'productos_ofrecidos' not in session:
        session['productos_ofrecidos'] = []
    
    proveedor = session.get('infoProveedor', {})
    if not proveedor:
        flash("No se ha agregado un proveedor.", "warning")
        return redirect(url_for('proveedores.nuevo'))
    
    if request.method == 'POST' and create_form.validate():        
        productos_ofrecidos = session.get('productos_ofrecidos', [])
        
        nuevo_producto = {
            'nombre_producto': create_form.nombre_producto.data,
            'cantidad': create_form.cantidad.data,
            'presentacion': create_form.presentacion.data,
            'precio_unitario': create_form.precio_unitario.data
        }
        
        productos_ofrecidos.append(nuevo_producto)
                
        session['productos_ofrecidos'] = productos_ofrecidos
        session.modified = True
        
        flash("Producto agregado.", "success")
        return redirect(url_for('proveedores.nuevoProductos'))

    return render_template("proveedores/nuevoProductos.html", form=create_form)    

@proveedores.route("/finalizar", methods=["GET", "POST"])
@login_required
@role_required('Cocinero', 'Administrador')
def finalizar():
    proveedor = session.get('infoProveedor', {})
    productos = session.get('productos_ofrecidos', [])

    if not proveedor:
        flash("No se ha agregado un proveedor.", "warning")
        return redirect(url_for('proveedores.nuevo'))
    
    if not productos:
        flash("No se han agregado productos.", "warning")
        return redirect(url_for('proveedores.nuevoProductos'))
    
    proveedor = Proveedor(
        nombre=proveedor['nombre'],
        telefono=proveedor['telefono'],
        direccion=proveedor['direccion']
    )
    db.session.add(proveedor)
    db.session.commit()
    
    for producto in productos:
        proveedor_producto = ProveedorProductos(
            idProveedores=proveedor.idProveedores,
            nombre_producto=producto['nombre_producto'],
            cantidad=producto['cantidad'],
            presentacion=producto['presentacion'],
            precio_unitario=producto['precio_unitario']
        )
        db.session.add(proveedor_producto)

    db.session.commit()
    
    session.pop('infoProveedor', None)
    session.pop('productos_ofrecidos', None)

    flash("Proveedor y productos guardados.", "success")
    return redirect(url_for('proveedores.nuevo'))

@proveedores.route("/cancelar", methods=["GET", "POST"])
@login_required
@role_required('Cocinero', 'Administrador')
def cancelar():    
    session.pop('infoProveedor', None) 
    session.pop('productos_ofrecidos', None) 
    flash("Operacion cancelada.", "warning")    
    return redirect(url_for('proveedores.nuevo'))

@proveedores.route("/ordenar", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def ordenar():
    
    proveedores = Proveedor.query.order_by(Proveedor.idProveedores).all()

    ordenes = Orden.query.filter_by(estatus='En Proceso').all()

    return render_template("proveedores/ordenar.html", proveedores=proveedores, ordenes=ordenes)

@proveedores.route("/guardarProveedor", methods=['POST'])
def guardarProveedor():   
    idProveedores = request.form.get('idProveedores')

    if idProveedores:
        session['idProveedores'] = idProveedores 
        flash("No se selecciono el proveedor.", "success")
        return redirect(url_for('proveedores.ordenarPedido')) 
    else:
        flash("No hay id del proveedor.", "warning")
        return redirect(url_for('proveedores.ordenar')) 

@proveedores.route("/ordenarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def ordenarPedido():
    create_form = forms.OrdenProveedorForm(request.form)

    if 'ordenNueva' not in session:
        session['ordenNueva'] = []    

    idProveedores = session.get('idProveedores')

    if not idProveedores:
        flash("Proveedor no seleccionado.", "warning")
        return redirect(url_for('proveedores.ordenar')) 

    proveedor = Proveedor.query.get(idProveedores)

    if not proveedor:
        flash("Proveedor no encontrado.", "warning")
        return redirect(url_for('proveedores.ordenar'))  

    productos = ProveedorProductos.query.filter_by(idProveedores=idProveedores).all()
    
    create_form.producto.choices = [
        (g.idProveedorProducto, f"{g.nombre_producto} - {g.cantidad} - {g.presentacion} - ${g.precio_unitario}") 
        for g in productos
    ]

    if request.method == 'POST' and create_form.validate():
        cantidad = create_form.cantidad.data
        idProducto = create_form.producto.data 
        ordenNueva = session.get('ordenNueva', [])
    
        producto_seleccionado = ProveedorProductos.query.filter_by(idProveedorProducto=idProducto, idProveedores=idProveedores).first() 
        
        if producto_seleccionado:
            nuevo_producto = {
                'nombre_producto': producto_seleccionado.nombre_producto,
                'cantidad': producto_seleccionado.cantidad,
                'presentacion': producto_seleccionado.presentacion,
                'precio_unitario': producto_seleccionado.precio_unitario,
                'cantidad_solicitada': cantidad
            }
        
            ordenNueva.append(nuevo_producto)
                    
            session['ordenNueva'] = ordenNueva
            session.modified = True
        
            flash("Producto agregado.", "success")
        else:
            flash("Producto no encontrado.", "warning")

        return redirect(url_for('proveedores.ordenarPedido'))

    return render_template("proveedores/ordenarPedido.html", proveedor=proveedor, productos=productos, form=create_form)

@proveedores.route("/cancelarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def cancelarPedido():
    session.pop('ordenNueva', None) 
    session.pop('idProveedores', None) 
    flash("Operacion cancelada.", "warning")    
    return redirect(url_for('proveedores.ordenar'))

@proveedores.route("/realizarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def realizarPedido():
    idProveedores = session.get('idProveedores')
    productos_orden = session.get('ordenNueva', [])

    if not idProveedores or not productos_orden:
        flash("No se puede realizar la orden. Faltan datos.", "warning")
        return redirect(url_for('proveedores.ordenar'))

    costo_total = sum(
        float(p['precio_unitario']) * float(p['cantidad_solicitada']) for p in productos_orden
    )
   
    nueva_orden = Orden(
        idProveedores=idProveedores,
        estatus='En Proceso',
        costo=costo_total
    )
    db.session.add(nueva_orden)
    db.session.commit() 
    
    for producto in productos_orden:        
        prod_bd = ProveedorProductos.query.filter_by(
            idProveedores=idProveedores,
            nombre_producto=producto['nombre_producto'],
            presentacion=producto['presentacion'],
            precio_unitario=producto['precio_unitario']
        ).first()

        if prod_bd:
            orden_producto = OrdenProductos(
                idOrdenes=nueva_orden.idOrdenes,
                idProveedorProducto=prod_bd.idProveedorProducto,
                cantidad_solicitada=producto['cantidad_solicitada'],
                costo_unitario=producto['precio_unitario'],
                presentacion=producto['presentacion']
            )
            db.session.add(orden_producto)

    db.session.commit()
    
    session.pop('ordenNueva', None)
    session.pop('idProveedores', None)

    flash("Orden registrada.", "success")
    return redirect(url_for('proveedores.ordenar'))

@proveedores.route("/ordenarRecibir", methods=['POST'])
@login_required
@role_required('Cocinero', 'Administrador')
def ordenarRecibir():
    idOrden = request.form.get('idOrdenes')
    orden = Orden.query.get(idOrden)

    if not orden:
        flash('Orden no encontrada', 'error')
        return redirect(url_for('proveedores.ordenar'))

    for item in orden.productos:
        fecha_caducidad = request.form.get(f'fecha_caducidad_{item.idOrdenProducto}')
        if not fecha_caducidad:
            flash(f'Ingrese la fecha de caducidad para todos los productos', 'error')
            return redirect(url_for('proveedores.ordenar'))

    for item in orden.productos:
        fecha_caducidad = request.form.get(f'fecha_caducidad_{item.idOrdenProducto}')
        item.fecha_caducidad = fecha_caducidad

        producto_proveedor = ProveedorProductos.query.filter_by(
            idProveedores=orden.proveedor.idProveedores,
            nombre_producto=item.producto.nombre_producto
        ).first()

        if not producto_proveedor:
            flash(f"No se encontró información del proveedor para {item.producto.nombre_producto}", 'error')
            return redirect(url_for('proveedores.ordenar'))

        cantidad_original = producto_proveedor.cantidad
        presentacion = producto_proveedor.presentacion
        precio_unitario = producto_proveedor.precio_unitario

        cantidad_convertida = cantidad_original
        unidad_final = presentacion

        if presentacion == "Kilos":
            cantidad_convertida = cantidad_original * 1000
            unidad_final = "Gramos"
        elif presentacion == "Litros":
            cantidad_convertida = cantidad_original * 1000
            unidad_final = "Mililitros"
        elif presentacion == "Gramos":
            unidad_final = "Gramos"
        elif presentacion == "Mililitros":
            unidad_final = "Mililitros"
        elif presentacion == "Piezas":
            unidad_final = "Piezas"

        materia_prima = MateriaPrima.query.filter_by(nombre=item.producto.nombre_producto).first()

        if materia_prima:
            materia_prima.cantidad += cantidad_convertida
            materia_prima.fecha_compra = datetime.today().date()
            materia_prima.fecha_caducidad = fecha_caducidad
            materia_prima.precio_unitario = precio_unitario
            materia_prima.cantidad_original = cantidad_convertida  # corregido
            materia_prima.presentacion = presentacion
        else:
            nueva_materia = MateriaPrima(
                nombre=item.producto.nombre_producto,
                cantidad=cantidad_convertida,
                cantidad_original=cantidad_convertida,  # corregido
                tipo=unidad_final,
                presentacion=presentacion,
                precio_unitario=precio_unitario,
                fecha_compra=datetime.today().date(),
                fecha_caducidad=fecha_caducidad,
                idProveedores=orden.proveedor.idProveedores
            )
            db.session.add(nueva_materia)

    orden.estatus = "Entregada"
    orden.fecha_entrega = datetime.today()

    db.session.commit()
    flash('Orden recibida correctamente.', 'success')
    return redirect(url_for('proveedores.ordenar'))