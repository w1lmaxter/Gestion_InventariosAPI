from app import db

class Proveedor(db.Model):
    """
    Modelo que representa un proveedor en el sistema.

    Cada proveedor tiene un nombre, un contacto, un teléfono y una dirección.

    Atributos:
        id_proveedor (int): Identificador único del proveedor (clave primaria).
        nombre (str): Nombre del proveedor.
        contacto (str): Nombre de la persona de contacto.
        telefono (str): Número de teléfono del proveedor.
        direccion (str): Dirección del proveedor.
    """
    
    __tablename__ = 'proveedores'

    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)

    def __init__(self, nombre, contacto, telefono, direccion):
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.direccion = direccion
