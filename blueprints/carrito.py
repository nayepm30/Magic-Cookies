from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import *
import forms

carrito = Blueprint('carrito', __name__)

@carrito.route("/check-session")
def check_session():
    """Verifica si el usuario está autenticado"""
    return jsonify({'isLoggedIn': current_user.is_authenticated})

@carrito.route("/carrito", methods=['GET', 'POST'])
@login_required
def funcion():
    """Página principal del carrito"""
    # Aquí iría la lógica para mostrar el carrito
    return render_template("carrito.html")

@carrito.route("/agregar", methods=['POST'])
@login_required
def agregar():
    """Agrega un producto al carrito"""
    try:
        # Obtener datos del formulario
        producto_id = request.form.get('producto_id')
        cantidad = request.form.get('cantidad', 1)
        
        # Aquí iría la lógica para agregar al carrito
        # ...
        
        return jsonify({
            'success': True,
            'message': 'Producto agregado al carrito'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400