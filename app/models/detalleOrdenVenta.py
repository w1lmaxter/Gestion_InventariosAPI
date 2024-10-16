from app import db

class DetalleOrdenVenta(db.Model):
    """
    Modelo que representa los detalles de una orden de venta en el sistema.

    Cada detalle de orden de venta está relacionado con una orden de venta y un producto.

    Atributos:
        - id_detalle_venta (int): Identificador único del detalle de orden de venta. Es la clave primaria, y no se puede repetir.
        - id_orden_venta (int): Identificador de la orden de venta a la que pertenece este detalle (clave foránea).
        - id_producto (int): Identificador del producto que está incluido en esta orden (clave foránea).
        - cantidad (int): Cantidad de productos específicos que están siendo vendidos en esta orden.
    """
    
    __tablename__ = 'detalle_orden_venta'  # El nombre de la tabla en la base de datos.

    id_detalle_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria, autoincremental.
    
    # Clave foránea que relaciona este detalle con una orden de venta.
    id_orden_venta = db.Column(db.Integer, db.ForeignKey('ordenes_venta.id_orden_venta'), nullable=False)
    
    # Clave foránea que relaciona este detalle con un producto específico.
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    
    cantidad = db.Column(db.Integer, nullable=True)  # Cantidad de ese producto en la orden de venta.

    # Relación con la tabla OrdenVenta. Cada detalle pertenece a una orden de venta.
    orden_venta = db.relationship('OrdenVenta', backref=db.backref('detalles_venta', lazy=True))
    
    # Relación con la tabla Producto. Cada detalle de orden está vinculado a un producto específico.
    producto = db.relationship('Producto', backref=db.backref('detalles_venta', lazy=True))

    def __init__(self, id_orden_venta, id_producto, cantidad):
        # Esta función inicializa los valores del detalle de orden de venta cuando se crea un nuevo registro.
        self.id_orden_venta = id_orden_venta
        self.id_producto = id_producto
        self.cantidad = cantidad