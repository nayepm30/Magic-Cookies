from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from models import *
import forms
from utils import role_required
from models import Producto, Carrito,Pedido, DetallePedido

carrito = Blueprint('carrito', __name__)

@carrito.route("/check-session")
def check_session():
    """Verifica si el usuario está autenticado"""
    return jsonify({
        'isLoggedIn': current_user.is_authenticated,  # ← Aquí se verifica
        'loginUrl': url_for('auth.login')
    })
    
@carrito.route("/galletas")
def mostrar_galletas():
    productos_raw = Producto.query.order_by(Producto.nombre, Producto.tipo).all()
    
    productos_agrupados = {}
    for producto in productos_raw:
        if producto.nombre not in productos_agrupados:
            productos_agrupados[producto.nombre] = {
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'peso': producto.peso,
                'imagen': producto.imagen,
                'presentaciones': []
            }
        
        # Mapeo de tipos a valores más legibles
        tipo_mapeado = {
            'Pieza': 'Pieza',
            'Pre-empaçada 700 gr': '700g',
            'Pre-empaçada 1Kg': '1kg'
        }.get(producto.tipo, producto.tipo)  # Usa el original si no está en el mapeo
        
        presentacion = {
            'tipo': producto.tipo,  # Guardamos el original para referencia
            'tipo_mostrar': tipo_mapeado,  # El valor legible para mostrar
            'precio': producto.precio
        }
            
        productos_agrupados[producto.nombre]['presentaciones'].append(presentacion)
    
    productos = list(productos_agrupados.values())
    return render_template("galletas.html", productos=productos)

@carrito.route("/carrito", methods=['GET'])
@login_required 
@role_required('Cliente')
def funcion():
    # Obtener items del carrito desde la base de datos
    cart_items = Carrito.query.filter_by(idUsuario=current_user.idUsuario).all()
    
    productos_data = []
    for item in cart_items:
        # Obtener la imagen del producto si está en la tabla de productos
        producto = Producto.query.get(item.idProducto)
        imagen = producto.imagen if producto and producto.imagen else item.imagen
        
        producto_data = {
            'id': item.idProducto,
            'nombre': item.nombre_producto,
            'presentacion': item.presentacion,
            'cantidad': item.cantidad,
            'precio_unitario': float(item.precio_unitario),
            'subtotal': float(item.subtotal),
            'imagen': imagen or "imagenes_productos/default.png"  # Imagen por defecto
        }
        productos_data.append(producto_data)

    total = sum(p['subtotal'] for p in productos_data)
    
    return render_template("carrito.html", productos=productos_data, total=total)

@carrito.route("/agregar/<int:producto_id>", methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    try:
        data = request.get_json()
        presentacion = data.get('presentacion')
        cantidad = int(data.get('cantidad', 1))
        precio = float(data.get('precio'))
        
        producto = db.session.get(Producto, producto_id)
        if not producto:
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404

        # Validar que la presentación es válida
        valid_presentations = ['Piezas', 'Pre-empacada 700 gr', 'Pre-empacada 1Kg']
        if presentacion not in valid_presentations:
            return jsonify({
                'success': False, 
                'error': f'Presentación no válida. Válidos: {valid_presentations}'
            }), 400

        # Verificar si el producto ya está en el carrito
        item = Carrito.query.filter_by(
            idUsuario=current_user.idUsuario,
            idProducto=producto_id,
            presentacion=presentacion
        ).first()

        if item:
            # Actualizar cantidad si ya existe
            item.cantidad += cantidad
            item.subtotal = float(item.precio_unitario) * item.cantidad
        else:
            # Crear nuevo item en el carrito
            nuevo_item = Carrito(
                idUsuario=current_user.idUsuario,
                idProducto=producto_id,
                nombre_producto=producto.nombre,
                presentacion=presentacion,
                cantidad=cantidad,
                precio_unitario=precio,
                imagen=producto.imagen
            )
            db.session.add(nuevo_item)
        
        db.session.commit()
        
        # Obtener el nuevo conteo del carrito
        carrito_count = Carrito.query.filter_by(idUsuario=current_user.idUsuario).count()
        
        return jsonify({
            'success': True,
            'cart_count': carrito_count
        })
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Datos numéricos no válidos'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@carrito.route("/actualizar", methods=['POST'])
@login_required
@role_required('Cliente')
def actualizar_carrito():
    try:
        data = request.get_json()
        producto_id = int(data.get('producto_id'))
        presentacion = data.get('presentacion')
        cantidad = int(data.get('cantidad'))
        
        # Buscar el item en el carrito
        item = Carrito.query.filter_by(
            idUsuario=current_user.idUsuario,
            idProducto=producto_id,
            presentacion=presentacion
        ).first()
        
        if item:
            if cantidad <= 0:
                # Eliminar si la cantidad es 0 o menos
                db.session.delete(item)
            else:
                # Actualizar cantidad y subtotal
                item.cantidad = cantidad
                item.subtotal = item.precio_unitario * cantidad
            db.session.commit()
            
            carrito_count = Carrito.query.filter_by(idUsuario=current_user.idUsuario).count()
            return jsonify({
                'success': True,
                'new_quantity': cantidad,
                'cart_count': carrito_count
            })
        
        return jsonify({'success': False, 'error': 'Producto no encontrado en el carrito'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@carrito.route("/eliminar/<int:producto_id>/<presentacion>", methods=['DELETE'])
@login_required
@role_required('Cliente')
def eliminar_del_carrito(producto_id, presentacion):
    try:
        item = Carrito.query.filter_by(
            idUsuario=current_user.idUsuario,
            idProducto=producto_id,
            presentacion=presentacion
        ).first()
        
        if item:
            db.session.delete(item)
            db.session.commit()
            
            carrito_count = Carrito.query.filter_by(idUsuario=current_user.idUsuario).count()
            return jsonify({
                'success': True,
                'cart_count': carrito_count
            })
        
        return jsonify({'success': False, 'error': 'Producto no encontrado en el carrito'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    

@carrito.route("/carrito-count")
@login_required
@role_required('Cliente')
def carrito_count():
    count = Carrito.query.filter_by(idUsuario=current_user.idUsuario).count()
    return jsonify({'count': count})

@carrito.route("/confirmar-pedido", methods=['POST'])
@login_required
@role_required('Cliente')
def confirmar_pedido():
    try:
        data = request.get_json()
        fecha_entrega = data.get('fecha_entrega')
        
        # 1. Obtener todos los items del carrito del usuario
        items_carrito = Carrito.query.filter_by(idUsuario=current_user.idUsuario).all()
        
        if not items_carrito:
            return jsonify({'success': False, 'error': 'El carrito está vacío'}), 400
        
        # 2. Crear el pedido principal
        nuevo_pedido = Pedido(
            idUsuario=current_user.idUsuario,
            fecha_pedido=db.func.now(),
            fecha_entrega=fecha_entrega,
            estatus='Pendiente'
        )
        db.session.add(nuevo_pedido)
        db.session.flush()  # Para obtener el idPedidos
        
        # 3. Crear los detalles del pedido y calcular el total
        total_pedido = 0
        for item in items_carrito:
            detalle = DetallePedido(
                idPedidos=nuevo_pedido.idPedidos,
                idProducto=item.idProducto,
                cantidad=item.cantidad,
                subtotal=item.subtotal
            )
            db.session.add(detalle)
            total_pedido += float(item.subtotal)
        
        # 4. Vaciar el carrito
        Carrito.query.filter_by(idUsuario=current_user.idUsuario).delete()
        
        # 5. Guardar todos los cambios
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido confirmado con éxito',
            'idPedido': nuevo_pedido.idPedidos,
            'total': total_pedido
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@carrito.route("/mis-pedidos")
@login_required
@role_required('Cliente')
def mis_pedidos():
    # Obtener pedidos con sus detalles y productos relacionados
    pedidos = Pedido.query\
        .filter_by(idUsuario=current_user.idUsuario)\
        .options(
            db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto)
        )\
        .order_by(Pedido.fecha_pedido.desc())\
        .all()
    
    # Calcular el total para cada pedido
    pedidos_con_total = []
    for pedido in pedidos:
        total = sum(float(detalle.subtotal) for detalle in pedido.detalles)
        pedidos_con_total.append({
            'pedido': pedido,
            'total': total
        })
    
    return render_template("mis_pedidos.html", pedidos=pedidos_con_total)

@carrito.route("/pedidos/<int:id_pedido>/cancelar", methods=['POST'])
@login_required
@role_required('Cliente')
def cancelar_pedido(id_pedido):
    try:
        pedido = Pedido.query.filter_by(
            idPedidos=id_pedido,
            idUsuario=current_user.idUsuario
        ).first()
        
        if not pedido:
            return jsonify({'success': False, 'error': 'Pedido no encontrado'}), 404
            
        if pedido.estatus != 'Pendiente':
            return jsonify({'success': False, 'error': 'Solo se pueden cancelar pedidos pendientes'}), 400
            
        pedido.estatus = 'Cancelado'
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@carrito.route("/ubicacion")
def ubicacion():
    return render_template("ubicacion.html")

@carrito.route("/sobre_nosotros")
def sobre_nosotros():
    return render_template("sobre_nosotros.html")