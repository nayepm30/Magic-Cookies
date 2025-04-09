from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
from flask_login import login_required
from models import *
from decimal import Decimal, ROUND_DOWN
from datetime import date
import os
import forms
from utils import role_required

ventas = Blueprint('ventas', __name__)

@ventas.route("/registrar", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def registrar():
    create_form = forms.nuevaVenta(request.form)    

    galletas = db.session.query(Producto.nombre).distinct().all()
    create_form.producto.choices = [(g.nombre, g.nombre) for g in galletas]
    
    if 'productos_seleccionados' not in session:
        session['productos_seleccionados'] = []
        
    if request.method == 'POST' and create_form.validate():
        pro = create_form.producto.data
        tip = create_form.presentacion.data
        cant = float(create_form.cantidad.data)
       
        galletaSelec = Producto.query.filter_by(nombre=pro, tipo=tip).first()

        if galletaSelec:
            
            cantidad_seleccionada = sum(
                p['cantidad'] for p in session['productos_seleccionados'] 
                if p['nombre'] == pro and p['tipo'] == tip
            )
            
            cantidad_disponible = galletaSelec.cantidad_stock - cantidad_seleccionada

            if cant <= cantidad_disponible:
                session['productos_seleccionados'].append({
                    'idProducto':galletaSelec.idProducto,
                    'nombre': galletaSelec.nombre,
                    'tipo': tip,
                    'cantidad': cant,
                    'precio': galletaSelec.precio,
                    'subtotal': float(galletaSelec.precio) * cant
                })
                session.modified = True 
                flash(f"Producto agregado.", "success")        
                #return redirect(url_for('ventas.registrar'))
            else:
                flash(f"No hay suficiente stock disponible. Solo quedan {cantidad_disponible}.", "danger")
                #return redirect(url_for('ventas.registrar'))   
        else:
            flash("Presentacion no disponible", "danger")           
            #return redirect(url_for('ventas.registrar'))
    
    return render_template("ventas/registrar.html", form=create_form)

@ventas.route("/finalizar", methods=["GET", "POST"])
@login_required
@role_required('Vendedor' , 'Administrador')
def finalizar():
    
    productos_seleccionados = session.get('productos_seleccionados', [])

    if productos_seleccionados:
        nueva_venta = Venta(fecha=date.today())

        db.session.add(nueva_venta)
        db.session.commit()

        id_venta = nueva_venta.idVenta

        total_venta = 0
        
        productos_vendidos = []

        for producto in productos_seleccionados:
            producto_db = Producto.query.get(producto['idProducto'])

            if producto_db and producto_db.cantidad_stock >= producto['cantidad']:
                producto_db.cantidad_stock -= producto['cantidad']

                detalle_venta = DetalleVenta(
                    idVenta=id_venta,
                    idProducto=producto['idProducto'],
                    cantidad=producto['cantidad'],
                    subtotal=producto['subtotal']
                )

                db.session.add(detalle_venta)
                total_venta += producto['subtotal']
                productos_vendidos.append(producto)
                db.session.commit()
            else:
                return jsonify({"status": "error", "message": f"Producto {producto_db.nombre} no tiene suficiente stock."})
            
        session['productos_finalizados'] = productos_vendidos
        session.pop('productos_seleccionados', None)
        
        
        ticket_folder = r"recibos"  
        if not os.path.exists(ticket_folder):
            os.makedirs(ticket_folder) 

        ticket_filename = f'ticket_venta_{id_venta}.txt'
        ticket_path = os.path.join(ticket_folder, ticket_filename)

        with open(ticket_path, 'w') as ticket_file:
            ticket_file.write(f"Ticket de Venta - ID: {id_venta}\n")
            ticket_file.write(f"Fecha: {date.today()}\n\n")
            ticket_file.write("Productos Vendidos:\n")
            for producto in productos_vendidos:
                ticket_file.write(f"{producto['cantidad']} x {producto['nombre']} - ${producto['subtotal']}\n")
            ticket_file.write("\n")
            ticket_file.write(f"Total Venta: ${total_venta:.2f}\n")
        
        return redirect(url_for('ventas.ticket'))

    else:
        flash("No hay productos seleccionados.", "danger")
        return redirect(url_for('ventas.registrar'))

@ventas.route("/historialFull", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def historialFull():
    ventas_detalles = []
    
    ventas = Venta.query.order_by(Venta.idVenta.desc()).all()
    
    for venta in ventas:
        detalles = DetalleVenta.query.filter_by(idVenta=venta.idVenta).all()
        detalle_venta = {
            'venta': venta,
            'detalles': [],
            'total': Decimal('0.00') 
        }
        
        for detalle in detalles:
            producto = Producto.query.get(detalle.idProducto)
            subtotal = Decimal(detalle.cantidad) * Decimal(producto.precio)  
            subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            
            detalle_venta['detalles'].append({
                'producto': producto,
                'cantidad': detalle.cantidad,
                'subtotal': subtotal
            })
            detalle_venta['total'] += subtotal     
        
        detalle_venta['total'] = detalle_venta['total'].quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        ventas_detalles.append(detalle_venta)
    return render_template('ventas/historialFull.html', ventas_detalles=ventas_detalles)

@ventas.route("/historialMini", methods=['GET'])
@login_required
@role_required('Vendedor' , 'Administrador')
def historialMini():
    ventas = Venta.query.order_by(Venta.idVenta.desc()).all()
    
    ventas = [
        {"idVenta": v.idVenta, "fecha": v.fecha, "total": v.total()} for v in ventas
    ]

    return render_template('ventas/historialMini.html', ventas=ventas)

@ventas.route("/detallesVenta", methods=["GET", "POST"])
@login_required
@role_required('Vendedor' , 'Administrador')
def detallesVenta(): 
    idVenta = request.form.get('idVenta')  
    
    if not idVenta:
        flash("No se proporcionó un ID de venta válido.", "error")
        return redirect(url_for('ventas.historialMini'))
    
    venta = Venta.query.get(idVenta)
    if not venta:
        flash("Venta no encontrada.", "error")
        return redirect(url_for('ventas.historialMini'))
    
    detalles_venta = DetalleVenta.query.filter_by(idVenta=idVenta).all()    
    
    total = sum(detalle.subtotal for detalle in detalles_venta)
    
    return render_template("ventas/historialDetalles.html", venta=venta, detalles_venta=detalles_venta, total=total)

@ventas.route("/ticket", methods=["GET", "POST"])
@login_required
@role_required('Vendedor' , 'Administrador')
def ticket():
    productos_finalizados = session.get('productos_finalizados', [])

    if not productos_finalizados:
        return redirect(url_for('ventas.registrar'))
    total = sum(float(producto['subtotal']) for producto in productos_finalizados)

    return render_template("ventas/ticket.html", productos=productos_finalizados, total=total)

@ventas.route("/volver", methods=["GET", "POST"])
@login_required
@role_required('Vendedor' , 'Administrador')
def volver():    
    session.pop('productos_finalizados', None)
    return redirect(url_for('ventas.registrar'))

@ventas.route("/cancelar", methods=["GET", "POST"])
@login_required
@role_required('Vendedor' , 'Administrador')
def cancelar():
    session.pop('productos_seleccionados', None) 
    flash("Venta cancelada.", "warning")
    return redirect(url_for('ventas.registrar'))

@ventas.route("/pedidos", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def pedidos():
        
    pedidos = Pedido.query.order_by(Pedido.idPedidos.desc()).all()
        
    return render_template("ventas/pedidos.html", pedidos=pedidos)

@ventas.route("/detalles", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def detalles(): 
    idPedido = request.form.get('idPedido')  

    pedido = Pedido.query.get(idPedido)
    if pedido:     
        usuario = Usuario.query.get(pedido.idUsuario)      
        detalles_pedido = DetallePedido.query.filter_by(idPedidos=pedido.idPedidos).all()      
        total = sum(detalle.subtotal for detalle in detalles_pedido)
        return render_template("ventas/pedidosDetalles.html", pedido=pedido, usuario=usuario, detalles_pedido=detalles_pedido, total=total)
    else:
        return redirect(url_for('ventas.pedidos'))

@ventas.route("/cancelarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def cancelarPedido():
    idPedido = request.form.get('idPedido')  

    pedido = Pedido.query.get(idPedido)
    if pedido:
        if pedido.estatus == "Pendiente":
            pedido.estatus = "Cancelado"  
            db.session.commit()  
            flash("Pedido cancelado.", "success")
        else: 
            if pedido.estatus == "Entregado":
                flash("No se puede cancelar un pedido entregado.", "danger")
            if pedido.estatus == "Cancelado":
                flash("El pedido ya fue cancelado.", "danger")
                
    return redirect(url_for('ventas.pedidos')) 

@ventas.route("/entregarPedido", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def entregarPedido():
    idPedido = request.form.get('idPedido')  

    pedido = Pedido.query.get(idPedido)
    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for('ventas.pedidos'))

    if pedido.estatus == "Cancelado":
        flash("No se puede entregar un pedido cancelado.", "danger")
        return redirect(url_for('ventas.pedidos'))
    
    if pedido.estatus == "Entregado":
        flash("El pedido ya fue entregado.", "danger")
        return redirect(url_for('ventas.pedidos'))

    detalles_pedido = DetallePedido.query.filter_by(idPedidos=pedido.idPedidos).all()

    # Verificamos si hay suficiente stock para los productos del pedido
    for detalle in detalles_pedido:
        producto = Producto.query.get(detalle.idProducto)
        
        if not producto:
            flash(f"El producto con ID {detalle.idProducto} no existe.", "danger")
            return redirect(url_for('ventas.pedidos'))

        if producto.cantidad_stock < detalle.cantidad:
            flash(f"No hay suficiente stock para el producto {producto.nombre}.", "danger")
            return redirect(url_for('ventas.pedidos'))

    # Creamos la venta
    nueva_venta = Venta(fecha=date.today())
    db.session.add(nueva_venta)
    db.session.commit()

    id_venta = nueva_venta.idVenta
    total_venta = 0

    # Creamos los detalles de la venta
    for detalle in detalles_pedido:
        producto = Producto.query.get(detalle.idProducto)
        subtotal = detalle.cantidad * producto.precio

        # Creamos el detalle de la venta
        detalle_venta = DetalleVenta(
            idVenta=id_venta,
            idProducto=detalle.idProducto,
            cantidad=detalle.cantidad,
            subtotal=subtotal
        )
        db.session.add(detalle_venta)

        # Descontamos el stock del producto
        producto.cantidad_stock -= detalle.cantidad
        db.session.commit()

        total_venta += subtotal

    # Actualizamos el estatus del pedido a "Entregado"
    pedido.estatus = "Entregado"
    db.session.commit()

    # Flash de éxito
    flash(f"Pedido entregado. Total venta: ${total_venta:.2f}", "success")

    return redirect(url_for('ventas.pedidos'))

@ventas.route("/productos", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def productos():
    
    productos = Producto.query.all()

    return render_template('ventas/productos.html', productos=productos)

@ventas.route("/corte", methods=['GET', 'POST'])
@login_required
@role_required('Vendedor' , 'Administrador')
def corte():
    if request.method == 'POST':
        
        fecha_actual = date.today()

        # Verificar si ya existe un corte para el día actual
        corte_existente = Ganancia.query.filter_by(fecha=fecha_actual).first()
        if corte_existente:
            flash("Ya se realizo el corte.", "warning")
            return redirect(url_for("ventas.corte"))

        # Calcular ventas totales
        ventas_totales = db.session.query(
            db.func.sum(DetalleVenta.subtotal)
        ).join(Venta).filter(Venta.fecha == fecha_actual).scalar() or 0

        # Calcular costos totales
        costos_totales = db.session.query(
            db.func.sum(DetalleVenta.cantidad * Producto.precio)
        ).join(Producto).join(Venta).filter(Venta.fecha == fecha_actual).scalar() or 0

        # Calcular utilidad bruta
        utilidad_bruta = ventas_totales - costos_totales

        # Gastos operativos (ajustado a 0)
        gastos_operativos = 0

        # Calcular utilidad neta
        utilidad_neta = utilidad_bruta - gastos_operativos

        # Crear un nuevo registro de corte (ganancia)
        nuevo_corte = Ganancia(
            fecha=fecha_actual,
            ventas_totales=ventas_totales,
            costos_totales=costos_totales,
            utilidad_bruta=utilidad_bruta,
            gastos_operativos=gastos_operativos,
            utilidad_neta=utilidad_neta
        )

        db.session.add(nuevo_corte)
        db.session.commit()

        flash("Corte realizado exitosamente.", "success")

    # Obtener todos los cortes realizados
    cortes = Ganancia.query.order_by(Ganancia.fecha.desc()).all()

    return render_template("ventas/corte.html", cortes=cortes)


