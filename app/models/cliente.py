from app import db

class Cliente(db.Model):
    """
    Modelo que representa un cliente en el sistema.

    Cada cliente tiene un nombre, un contacto, un teléfono y una dirección.

    Atributos:
        id_cliente (int): Identificador único del cliente (clave primaria).
        nombre (str): Nombre del cliente.
        contacto (str): Nombre de la persona de contacto.
        telefono (str): Número de teléfono del cliente.
        direccion (str): Dirección del cliente.
    """
    
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)

    def __init__(self, nombre, contacto, telefono, direccion):
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.direccion = direccion