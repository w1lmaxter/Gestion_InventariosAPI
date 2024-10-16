from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.detalleOrdenCompra import DetalleOrdenCompra  # Importa el modelo DetalleOrdenCompra.
from app.models.ordenCompra import OrdenCompra  # Importa el modelo OrdenCompra.
from app.models.producto import Producto  # Importa el modelo Producto.

class DetalleOrdenCompraService:
    @staticmethod
    def create_detalle_orden_compra(id_orden_compra, id_producto, cantidad):
        """
        Crear un nuevo detalle de orden de compra.
        
        Args:
            id_orden_compra (int): ID de la orden de compra.
            id_producto (int): ID del producto.
            cantidad (int): Cantidad del producto.
        
        Returns:
            DetalleOrdenCompra: El detalle de la orden de compra creado.
        """
        # Busca la orden de compra por su ID.
        orden_compra = OrdenCompra.query.get(id_orden_compra)
        if not orden_compra:  # Si no se encuentra la orden de compra, lanza un error.
            raise ValueError("La orden de compra especificada no existe.")
        
        # Busca el producto por su ID.
        producto = Producto.query.get(id_producto)
        if not producto:  # Si no se encuentra el producto, lanza un error.
            raise ValueError("El producto especificado no existe.")

        # Crea una nueva instancia de DetalleOrdenCompra con los datos proporcionados.
        detalle = DetalleOrdenCompra(id_orden_compra=id_orden_compra, id_producto=id_producto, cantidad=cantidad)
        db.session.add(detalle)  # Agrega el nuevo detalle a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return detalle  # Retorna el detalle de la orden de compra creado.

    @staticmethod
    def get_detalles_orden_compra(id_orden_compra):
        """
        Obtener todos los detalles de una orden de compra específica.
        
        Args:
            id_orden_compra (int): ID de la orden de compra.
        
        Returns:
            List[DetalleOrdenCompra]: Lista de detalles de la orden de compra.
        """
        # Devuelve todos los detalles asociados a la orden de compra especificada.
        return DetalleOrdenCompra.query.filter_by(id_orden_compra=id_orden_compra).all()

    @staticmethod
    def get_all_detalles_orden_compra():
        """
        Obtener todos los detalles de orden de compra.
        
        Returns:
            List[DetalleOrdenCompra]: Lista de todos los detalles de orden de compra.
        """
        # Devuelve todos los detalles de orden de compra almacenados en la base de datos.
        return DetalleOrdenCompra.query.all()

    @staticmethod
    def update_detalle_orden_compra(id_detalle, id_producto, cantidad):
        """
        Actualizar un detalle de orden de compra existente.
        
        Args:
            id_detalle (int): ID del detalle de orden de compra a actualizar.
            id_producto (int): Nuevo ID del producto.
            cantidad (int): Nueva cantidad del producto.

        Returns:
            DetalleOrdenCompra: Detalle de orden de compra actualizado.
        """
        # Busca el detalle de orden de compra por su ID.
        detalle = DetalleOrdenCompra.query.get(id_detalle)
        if detalle is None:  # Si no se encuentra el detalle, lanza un error.
            raise ValueError("El detalle de orden de compra no existe.")

        # Busca el producto por su ID.
        producto = Producto.query.get(id_producto)
        if not producto:  # Si no se encuentra el producto, lanza un error.
            raise ValueError("El producto especificado no existe.")

        # Actualiza los campos del detalle.
        detalle.id_producto = id_producto
        detalle.cantidad = cantidad
        db.session.commit()  # Confirma los cambios en la base de datos.
        return detalle  # Retorna el detalle de orden de compra actualizado.

    @staticmethod
    def delete_detalle_orden_compra(id_detalle):
        """
        Eliminar un detalle de orden de compra por su ID.

        Args:
            id_detalle (int): ID del detalle a eliminar.

        Raises:
            ValueError: Si el detalle no se encuentra.
        """
        # Busca el detalle de orden de compra por su ID.
        detalle = DetalleOrdenCompra.query.get(id_detalle)
        if detalle is None:  # Si no se encuentra el detalle, lanza un error.
            raise ValueError("El detalle de orden de compra no existe.")
        
        db.session.delete(detalle)  # Elimina el detalle de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.