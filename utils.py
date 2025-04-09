# utils.py
from functools import wraps
from flask_login import current_user
from flask import abort, flash, redirect, url_for

def role_required(*roles):
    """
    Decorador para restringir acceso a usuarios con roles específicos.
    Ejemplo: @role_required('Administrador', 'Vendedor')
    """
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if current_user.is_anonymous or current_user.rol not in roles:
                flash("Acceso denegado: no tienes los permisos necesarios.", "danger")
                return redirect(url_for('inicio.dashboard'))  # Redirige al login o a la página deseada
            return f(*args, **kwargs)
        return wrapped_function
    return decorator
