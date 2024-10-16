from app import db


class DetalleOrdenCompra(db.Model):
    """
    Modelo que representa los detalles de una orden de compra en el sistema.

    Cada detalle de orden de compra está relacionado con una orden de compra y un producto.

    Atributos:
        - id_detalle_compra (int): Identificador único del detalle de orden de compra. Es la clave primaria, y no se puede repetir.
        - id_orden_compra (int): Identificador de la orden de compra a la que pertenece este detalle (clave foránea).
        - id_producto (int): Identificador del producto que está siendo comprado en esta orden (clave foránea).
        - cantidad (int): Cantidad del producto que se está comprando en la orden de compra.
    """

    __tablename__ = "detalle_orden_compra"  # Nombre de la tabla en la base de datos.

    id_detalle_compra = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )  # Clave primaria, autoincremental.

    # Clave foránea que relaciona este detalle con una orden de compra.
    id_orden_compra = db.Column(
        db.Integer, db.ForeignKey("ordenes_compra.id_orden_compra"), nullable=False
    )

    # Clave foránea que relaciona este detalle con un producto específico.
    id_producto = db.Column(
        db.Integer, db.ForeignKey("productos.id_producto"), nullable=False
    )

    cantidad = db.Column(
        db.Integer, nullable=True
    )  # Cantidad del producto que se está comprando.

    # Relación con la tabla OrdenCompra. Cada detalle pertenece a una orden de compra.
    orden_compra = db.relationship(
        "OrdenCompra", backref=db.backref("detalles_compra", lazy=True)
    )

    # Relación con la tabla Producto. Cada detalle de orden está vinculado a un producto específico.
    producto = db.relationship(
        "Producto", backref=db.backref("detalles_compra", lazy=True)
    )

    def __init__(self, id_orden_compra, id_producto, cantidad):
        # Esta función inicializa los valores del detalle de orden de compra cuando se crea un nuevo registro.
        self.id_orden_compra = id_orden_compra
        self.id_producto = id_producto
        self.cantidad = cantidad
