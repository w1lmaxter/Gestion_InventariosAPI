from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.proveedor import Proveedor  # Importa el modelo Proveedor.

class ProveedorService:
    @staticmethod
    def create_proveedor(nombre, contacto, telefono, direccion):
        """
        Crear un nuevo proveedor.
        
        Args:
            nombre (str): Nombre del proveedor.
            contacto (str): Nombre de la persona de contacto.
            telefono (str): Número de teléfono del proveedor.
            direccion (str): Dirección del proveedor.
        
        Returns:
            Proveedor: El proveedor creado.
        """
        # Verifica que todos los campos sean proporcionados. Si falta alguno, lanza un error.
        if not all([nombre, contacto, telefono, direccion]):
            raise ValueError("Todos los campos son obligatorios.")
        
        # Crea una nueva instancia de Proveedor con los datos proporcionados.
        proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono, direccion=direccion)
        db.session.add(proveedor)  # Agrega el nuevo proveedor a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return proveedor  # Retorna el proveedor creado.

    @staticmethod
    def get_all_proveedores():
        """
        Obtener todos los proveedores de la base de datos.
        
        Returns:
            List[Proveedor]: Lista de todos los proveedores.
        """
        # Devuelve todos los proveedores almacenados en la base de datos.
        return Proveedor.query.all()  # Utiliza el método query de SQLAlchemy para obtener todos los registros.

    @staticmethod
    def update_proveedor(id_proveedor, new_data):
        """
        Actualizar los datos de un proveedor existente.
        
        Args:
            id_proveedor (int): ID del proveedor a actualizar.
            new_data (dict): Diccionario con los nuevos datos.
        
        Returns:
            Proveedor: El proveedor actualizado.
        """
        # Busca el proveedor por su ID en la base de datos.
        proveedor = Proveedor.query.get(id_proveedor)
        if not proveedor:  # Si no se encuentra el proveedor, lanza un error.
            raise ValueError('Proveedor no encontrado')
        
        # Actualiza los atributos del proveedor con los nuevos datos proporcionados.
        for key, value in new_data.items():
            if hasattr(proveedor, key):  # Verifica si el proveedor tiene el atributo que se quiere actualizar.
                setattr(proveedor, key, value)  # Actualiza el atributo con el nuevo valor.
        
        db.session.commit()  # Confirma los cambios en la base de datos.
        return proveedor  # Retorna el proveedor actualizado.

    @staticmethod
    def delete_proveedor(id_proveedor):
        """
        Eliminar un proveedor existente.
        
        Args:
            id_proveedor (int): ID del proveedor a eliminar.
        
        Returns:
            None
        """
        # Busca el proveedor por su ID en la base de datos.
        proveedor = Proveedor.query.get(id_proveedor)
        if not proveedor:  # Si no se encuentra el proveedor, lanza un error.
            raise ValueError('Proveedor no encontrado')
        
        db.session.delete(proveedor)  # Elimina el proveedor de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.