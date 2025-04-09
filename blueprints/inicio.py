from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Producto, DetalleVenta, Venta
from sqlalchemy import func

# Cambia el nombre del Blueprint a 'inicio_bp'
inicio = Blueprint('inicio', __name__)

@inicio.route("/inicio", methods=['GET', 'POST'])
@login_required
def dashboard():
    productos_mas_vendidos = db.session.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label('total_vendido')
    ).join(DetalleVenta, Producto.idProducto == DetalleVenta.idProducto).group_by(Producto.idProducto).order_by(func.sum(DetalleVenta.cantidad).desc()).limit(5).all()

    presentaciones_mas_vendidas = db.session.query(
        Producto.tipo,
        func.sum(DetalleVenta.cantidad).label('total_vendido')
    ).join(DetalleVenta, Producto.idProducto == DetalleVenta.idProducto).group_by(Producto.tipo).order_by(func.sum(DetalleVenta.cantidad).desc()).limit(5).all()

    ventas_diarias = db.session.query(
        func.sum(DetalleVenta.subtotal).label('total_ventas_diarias')
    ).join(Venta, Venta.idVenta == DetalleVenta.idVenta).filter(Venta.fecha == func.curdate()).all()

    total_ventas_diarias = ventas_diarias[0][0] if ventas_diarias else 0  

    return render_template(
        "dashboard.html",
        productos_mas_vendidos=productos_mas_vendidos,
        presentaciones_mas_vendidas=presentaciones_mas_vendidas,
        total_ventas_diarias=total_ventas_diarias
    )