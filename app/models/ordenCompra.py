from app import db

class OrdenCompra(db.Model):
    """
    Modelo que representa una orden de compra en el sistema.

    Cada orden de compra está relacionada con un proveedor y tiene un estado.

    Atributos:
        - id_orden_compra (int): Es el identificador único de la orden de compra. Es la clave primaria (primary key), lo que significa que no puede repetirse.
        - fecha_inicio (date): La fecha en que la orden de compra empezó o fue creada.
        - fecha_final (date): La fecha en que la orden de compra finalizó.
        - estado (str): Indica en qué estado está la orden, como "completado", "pendiente" o "cancelado".
        - id_proveedor (int): El identificador del proveedor asociado a la orden (clave foránea), que conecta con la tabla de proveedores.
    """
    
    __tablename__ = 'ordenes_compra'  # Nombre de la tabla en la base de datos.

    # Aquí definimos las columnas de la tabla
    id_orden_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria, autoincremental.
    fecha_inicio = db.Column(db.Date, nullable=True)  # Fecha de inicio de la orden de compra, opcional.
    fecha_final = db.Column(db.Date, nullable=True)  # Fecha de finalización de la orden de compra, también opcional.
    estado = db.Column(db.Enum('completado', 'pendiente', 'cancelado'), nullable=True)  # Estado de la orden.
    
    # id_proveedor es una clave foránea que vincula esta tabla con la tabla de proveedores.
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    # El campo `ForeignKey('proveedores.id_proveedor')` crea la relación con la tabla proveedores, vinculando la orden con el proveedor específico.

    # La relación con el modelo Proveedor, lo que permite acceder a los datos del proveedor desde la orden de compra.
    proveedor = db.relationship('Proveedor', backref=db.backref('ordenes_compra', lazy=True))  

    def __init__(self, fecha_inicio, fecha_final, estado, id_proveedor):
        # Esta es la función que se ejecuta cuando se crea una nueva instancia de OrdenCompra.
        # Se inicializan las fechas, el estado y el proveedor.
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.estado = estado
        self.id_proveedor = id_proveedor