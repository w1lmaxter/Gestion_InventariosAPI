from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.producto import Producto  # Importa el modelo Producto.

class ProductoService:
    @staticmethod
    def create_producto(nombre, costo, precio_venta, cantidad):
        """
        Crear un nuevo producto.
        
        Args:
            nombre (str): Nombre del producto.
            costo (float): Costo del producto.
            precio_venta (float): Precio de venta del producto.
            cantidad (int): Cantidad disponible del producto.
        
        Returns:
            Producto: El producto creado.
        """
        # Crea una nueva instancia de Producto con los datos proporcionados.
        producto = Producto(nombre=nombre, costo=costo, precio_venta=precio_venta, cantidad=cantidad)
        db.session.add(producto)  # Agrega el nuevo producto a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return producto  # Retorna el producto creado.

    @staticmethod
    def get_all_productos():
        """
        Obtener todos los productos de la base de datos.
        
        Returns:
            List[Producto]: Lista de todos los productos.
        """
        # Devuelve todos los productos almacenados en la base de datos.
        return Producto.query.all()  # Utiliza el método query de SQLAlchemy para obtener todos los registros.

    @staticmethod
    def update_producto(id_producto, new_data):
        """
        Actualizar los datos de un producto existente.
        
        Args:
            id_producto (int): ID del producto a actualizar.
            new_data (dict): Diccionario con los nuevos datos.
        
        Returns:
            Producto: El producto actualizado.
        """
        # Busca el producto por su ID en la base de datos.
        producto = Producto.query.get(id_producto)
        if not producto:  # Si no se encuentra el producto, lanza un error.
            raise ValueError('Producto no encontrado')

        # Actualiza los atributos del producto con los nuevos datos proporcionados.
        for key, value in new_data.items():
            if hasattr(producto, key):  # Verifica si el producto tiene el atributo que se quiere actualizar.
                setattr(producto, key, value)  # Actualiza el atributo con el nuevo valor.

        db.session.commit()  # Confirma los cambios en la base de datos.
        return producto  # Retorna el producto actualizado.

    @staticmethod
    def delete_producto(id_producto):
        """
        Eliminar un producto existente.
        
        Args:
            id_producto (int): ID del producto a eliminar.
        
        Returns:
            None
        """
        # Busca el producto por su ID en la base de datos.
        producto = Producto.query.get(id_producto)
        if not producto:  # Si no se encuentra el producto, lanza un error.
            raise ValueError('Producto no encontrado')
        
        db.session.delete(producto)  # Elimina el producto de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.