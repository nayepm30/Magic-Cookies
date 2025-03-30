from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'tbl_usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    telefono = db.Column(db.String(15))
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Administrador', 'Vendedor', 'Cocinero', 'Cliente'), nullable=False)
    
    def get_id(self):
        return str(self.idUsuario)
    
# Tabla de Productos
class Producto(db.Model):
    __tablename__ = 'tbl_productos'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('Piezas', 'Pre-empacada 700 gr', 'Pre-empacada 1Kg', 'Gramos'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad_stock = db.Column(db.Integer, nullable=False)
    fecha_caducidad = db.Column(db.Date)
    peso = db.Column(db.Numeric(10, 2))
    fecha_produccion = db.Column(db.DateTime)

# Tabla de Ventas
class Venta(db.Model):
    __tablename__ = 'tbl_ventas'
    idVenta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)

# Tabla de Detalles de Ventas
class DetalleVenta(db.Model):
    __tablename__ = 'tbl_detalle_ventas'
    idDetalle = db.Column(db.Integer, primary_key=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('tbl_ventas.idVenta'))
    idProducto = db.Column(db.Integer, db.ForeignKey('tbl_productos.idProducto'))
    cantidad = db.Column(db.Numeric(10, 2))
    subtotal = db.Column(db.Numeric)

# Tabla de Pedidos
class Pedido(db.Model):
    __tablename__ = 'tbl_pedidos'
    idPedidos = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('tbl_usuarios.idUsuario'))
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    fecha_entrega = db.Column(db.DateTime)
    estatus = db.Column(db.Enum('Pendiente', 'Entregado', 'Cancelado'), nullable=False)

# Tabla de Detalles de Pedido
class DetallePedido(db.Model):
    __tablename__ = 'tbl_detalles_pedido'
    idDetalle = db.Column(db.Integer, primary_key=True)
    idPedidos = db.Column(db.Integer, db.ForeignKey('tbl_pedidos.idPedidos'))
    idProducto = db.Column(db.Integer, db.ForeignKey('tbl_productos.idProducto'))
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Numeric)

# Tabla de Proveedores
class Proveedor(db.Model):
    __tablename__ = 'tbl_proveedores'
    idProveedores = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    telefono = db.Column(db.String(45))
    direccion = db.Column(db.String(45))

# Tabla de Materia Prima
class MateriaPrima(db.Model):
    __tablename__ = 'tbl_materia_prima'
    idIngrediente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('Piezas', 'Litros', 'Gramos', 'Kilos'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2))
    fecha_compra = db.Column(db.Date)
    precio = db.Column(db.Numeric(10, 2))
    idProveedores = db.Column(db.Integer, db.ForeignKey('tbl_proveedores.idProveedores'))

# Tabla de Recetas
class Receta(db.Model):
    __tablename__ = 'tbl_recetas'
    idReceta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    cantidad_produccion = db.Column(db.Integer)

# Tabla de Relación Receta-Ingredientes
class RecetaIngrediente(db.Model):
    __tablename__ = 'tbl_receta_ingredientes'
    idDetalle = db.Column(db.Integer, primary_key=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('tbl_recetas.idReceta'))
    idIngrediente = db.Column(db.Integer, db.ForeignKey('tbl_materia_prima.idIngrediente'))
    cantidad = db.Column(db.Numeric(10, 2))

# Tabla de Mermas
class Merma(db.Model):
    __tablename__ = 'tbl_mermas'
    idMerma = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('Productos', 'Insumos'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2))
    motivo = db.Column(db.Text)
    idProducto = db.Column(db.Integer, db.ForeignKey('tbl_productos.idProducto'))
    idIngrediente = db.Column(db.Integer, db.ForeignKey('tbl_materia_prima.idIngrediente'))

# Tabla de Ganancias
class Ganancia(db.Model):
    __tablename__ = 'tbl_ganancias'
    idGanancia = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    ventas_totales = db.Column(db.Numeric(10, 2))
    costos_totales = db.Column(db.Numeric(10, 2))
    utilidad_bruta = db.Column(db.Numeric(10, 2))
    gastos_operativos = db.Column(db.Numeric(10, 2))
    utilidad_neta = db.Column(db.Numeric(10, 2))
