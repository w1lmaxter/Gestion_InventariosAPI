from app import db

class OrdenVenta(db.Model):
    """
    Modelo que representa una orden de venta en el sistema.
    
    Cada orden de venta está relacionada con un cliente y tiene un estado.
    
    Atributos:
        - id_orden_venta (int): Es el identificador único de la orden de venta. Es la clave primaria (primary key), lo que significa que no puede repetirse.
        - fecha_inicio (date): La fecha en que la orden de venta empezó o fue creada.
        - fecha_final (date): La fecha en que la orden de venta finalizó.
        - estado (str): Indica en qué estado está la orden, como si está "completado", "pendiente" o "cancelado".
        - id_cliente (int): El identificador del cliente al que pertenece esta orden de venta. Este campo es una clave foránea (foreign key), lo que significa que se relaciona con la tabla de clientes.
    """
    
    __tablename__ = 'ordenes_venta'  # Nombre de la tabla en la base de datos que almacenará las órdenes de venta.

    # Aquí estamos definiendo los campos que tendrá la tabla en la base de datos
    id_orden_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria, autoincremental (se genera automáticamente).
    fecha_inicio = db.Column(db.Date, nullable=True)  # La fecha cuando comienza la orden de venta, este campo es opcional (puede ser nulo).
    fecha_final = db.Column(db.Date, nullable=True)  # La fecha cuando se completa o finaliza la orden de venta, también opcional.
    estado = db.Column(db.Enum('completado', 'pendiente', 'cancelado'), nullable=True)  # El estado de la orden: puede ser completado, pendiente o cancelado.
    
    # Este campo es clave foránea, vincula esta tabla con la tabla "clientes"
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)  
    # "ForeignKey('clientes.id_cliente')" indica que este campo está vinculado a la columna "id_cliente" de la tabla "clientes".
    # Esto crea una relación entre la orden de venta y el cliente.

    # Esta línea crea la relación entre la orden de venta y el cliente. El objeto "cliente" te permitirá acceder a los datos del cliente.
    # El parámetro backref permite acceder a todas las órdenes de venta desde el modelo Cliente.
    cliente = db.relationship('Cliente', backref=db.backref('ordenes_venta', lazy=True))  

    def __init__(self, fecha_inicio, fecha_final, estado, id_cliente):
        # Esta es la función que se ejecuta cuando se crea una nueva instancia de OrdenVenta.
        # Se le pasan los datos necesarios para inicializar el objeto (fecha de inicio, fecha final, estado y cliente).
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.estado = estado
        self.id_cliente = id_cliente