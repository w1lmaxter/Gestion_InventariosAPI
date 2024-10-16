from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.detalleOrdenVenta import DetalleOrdenVenta  # Importa el modelo DetalleOrdenVenta.
from app.models.ordenVenta import OrdenVenta  # Importa el modelo OrdenVenta.
from app.models.producto import Producto  # Importa el modelo Producto.

class DetalleOrdenVentaService:
    @staticmethod
    def create_detalle_orden_venta(id_orden_venta, id_producto, cantidad):
        """
        Crear un nuevo detalle de orden de venta.
        
        Args:
            id_orden_venta (int): ID de la orden de venta.
            id_producto (int): ID del producto.
            cantidad (int): Cantidad del producto.
        
        Returns:
            DetalleOrdenVenta: El detalle de la orden de venta creado.
        """
        # Busca la orden de venta por su ID.
        orden_venta = OrdenVenta.query.get(id_orden_venta)
        if not orden_venta:  # Si no se encuentra la orden de venta, lanza un error.
            raise ValueError("La orden de venta especificada no existe.")
        
        # Busca el producto por su ID.
        producto = Producto.query.get(id_producto)
        if not producto:  # Si no se encuentra el producto, lanza un error.
            raise ValueError("El producto especificado no existe.")

        # Crea una nueva instancia de DetalleOrdenVenta con los datos proporcionados.
        detalle = DetalleOrdenVenta(id_orden_venta=id_orden_venta, id_producto=id_producto, cantidad=cantidad)
        db.session.add(detalle)  # Agrega el nuevo detalle a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return detalle  # Retorna el detalle de la orden de venta creado.

    @staticmethod
    def get_detalles_orden_venta(id_orden_venta):
        """
        Obtener todos los detalles de una orden de venta específica.
        
        Args:
            id_orden_venta (int): ID de la orden de venta.
        
        Returns:
            List[DetalleOrdenVenta]: Lista de detalles de la orden de venta.
        """
        # Devuelve todos los detalles asociados a la orden de venta especificada.
        return DetalleOrdenVenta.query.filter_by(id_orden_venta=id_orden_venta).all()

    @staticmethod
    def get_all_detalles_orden_venta():
        """
        Obtener todos los detalles de orden de venta.
        
        Returns:
            List[DetalleOrdenVenta]: Lista de todos los detalles de orden de venta.
        """
        # Devuelve todos los detalles de orden de venta almacenados en la base de datos.
        return DetalleOrdenVenta.query.all()

    @staticmethod
    def update_detalle_orden_venta(id_detalle_venta, data):
        """
        Actualizar un detalle de orden de venta existente.
        
        Args:
            id_detalle_venta (int): ID del detalle de orden de venta.
            data (dict): Datos a actualizar.
        
        Returns:
            DetalleOrdenVenta: El detalle de orden de venta actualizado.
        
        Raises:
            ValueError: Si el detalle no se encuentra.
        """
        # Busca el detalle de orden de venta por su ID.
        detalle = DetalleOrdenVenta.query.get(id_detalle_venta)
        if detalle is None:  # Si no se encuentra el detalle, lanza un error.
            raise ValueError("El detalle de orden de venta no existe.")
        
        # Actualiza los campos basados en el diccionario
        detalle.id_orden_venta = data.get('id_orden_venta', detalle.id_orden_venta)
        detalle.id_producto = data.get('id_producto', detalle.id_producto)
        detalle.cantidad = data.get('cantidad', detalle.cantidad)

        db.session.commit()  # Confirma los cambios en la base de datos.
        return detalle  # Retorna el detalle de orden de venta actualizado.

    @staticmethod
    def delete_detalle_orden_venta(id_detalle):
        """
        Eliminar un detalle de orden de venta por su ID.

        Args:
            id_detalle (int): ID del detalle a eliminar.

        Raises:
            ValueError: Si el detalle no se encuentra.
        """
        # Busca el detalle de orden de venta por su ID.
        detalle = DetalleOrdenVenta.query.get(id_detalle)
        if detalle is None:  # Si no se encuentra el detalle, lanza un error.
            raise ValueError("El detalle de orden de venta no existe.")
        
        db.session.delete(detalle)  # Elimina el detalle de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.