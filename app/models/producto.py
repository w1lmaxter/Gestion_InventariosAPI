from app import db

class Producto(db.Model):
    """
    Modelo que representa un producto en el sistema.

    Cada producto tiene un nombre, costo, precio de venta y cantidad disponible.

    Atributos:
        id_producto (int): Identificador único del producto (clave primaria).
        nombre (str): Nombre del producto.
        costo (float): Costo del producto.
        precio_venta (float): Precio de venta del producto.
        cantidad (int): Cantidad disponible del producto.
    """
    
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    costo = db.Column(db.Numeric(10, 2), nullable=True)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad = db.Column(db.Integer, nullable=True)

    def __init__(self, nombre, costo, precio_venta, cantidad):
        self.nombre = nombre
        self.costo = costo
        self.precio_venta = precio_venta
        self.cantidad = cantidad
