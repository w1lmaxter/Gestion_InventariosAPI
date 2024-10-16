from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.cliente import Cliente  # Importa el modelo Cliente.

class ClienteService:
    @staticmethod
    def create_cliente(nombre, contacto, telefono, direccion):
        """
        Crear un nuevo cliente.
        
        Args:
            nombre (str): Nombre del cliente.
            contacto (str): Nombre de la persona de contacto.
            telefono (str): Número de teléfono del cliente.
            direccion (str): Dirección del cliente.
        
        Returns:
            Cliente: El cliente creado.
        """
        # Verifica que todos los campos obligatorios están presentes.
        if not all([nombre, contacto, telefono, direccion]):
            raise ValueError("Todos los campos son obligatorios.")
        
        # Crea una nueva instancia de Cliente con los datos proporcionados.
        cliente = Cliente(nombre=nombre, contacto=contacto, telefono=telefono, direccion=direccion)
        db.session.add(cliente)  # Agrega el nuevo cliente a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return cliente  # Retorna el cliente creado.

    @staticmethod
    def get_all_clientes():
        """
        Obtener todos los clientes de la base de datos.
        
        Returns:
            List[Cliente]: Lista de todos los clientes.
        """
        # Devuelve todos los clientes almacenados en la base de datos.
        return Cliente.query.all()

    @staticmethod
    def update_cliente(id_cliente, new_data):
        """
        Actualizar los datos de un cliente existente.
        
        Args:
            id_cliente (int): ID del cliente a actualizar.
            new_data (dict): Diccionario con los nuevos datos.
        
        Returns:
            Cliente: El cliente actualizado.
        """
        # Busca el cliente por su ID.
        cliente = Cliente.query.get(id_cliente)
        if not cliente:  # Si no se encuentra el cliente, lanza un error.
            raise ValueError('Cliente no encontrado')

        # Actualiza los campos basados en el diccionario new_data.
        for key, value in new_data.items():
            if hasattr(cliente, key):  # Verifica si el cliente tiene el atributo a actualizar.
                setattr(cliente, key, value)  # Actualiza el atributo con el nuevo valor.
        
        db.session.commit()  # Confirma los cambios en la base de datos.
        return cliente  # Retorna el cliente actualizado.

    @staticmethod
    def delete_cliente(id_cliente):
        """
        Eliminar un cliente existente.
        
        Args:
            id_cliente (int): ID del cliente a eliminar.
        
        Returns:
            None
        """
        # Busca el cliente por su ID.
        cliente = Cliente.query.get(id_cliente)
        if not cliente:  # Si no se encuentra el cliente, lanza un error.
            raise ValueError('Cliente no encontrado')

        db.session.delete(cliente)  # Elimina el cliente de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.