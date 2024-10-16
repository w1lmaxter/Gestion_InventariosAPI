from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.ordenVenta import OrdenVenta  # Importa el modelo OrdenVenta.
from app.models.cliente import Cliente  # Importa el modelo Cliente.

class OrdenVentaService:
    @staticmethod
    def create_orden_venta(fecha_inicio, fecha_final, estado, id_cliente):
        """
        Crear una nueva orden de venta.
        
        Args:
            fecha_inicio (date): Fecha de inicio de la orden.
            fecha_final (date): Fecha final de la orden.
            estado (str): Estado de la orden.
            id_cliente (int): ID del cliente asociado a la orden.
        
        Returns:
            OrdenVenta: La orden de venta creada.
        """
        # Verifica que todos los campos requeridos estén presentes.
        if not all([fecha_inicio, fecha_final, estado, id_cliente]):
            raise ValueError("Todos los campos son obligatorios.")
        
        # Busca el cliente por su ID.
        cliente = Cliente.query.get(id_cliente)
        if not cliente:  # Si no se encuentra el cliente, lanza un error.
            raise ValueError("El cliente especificado no existe.")
        
        # Lista de estados válidos para la orden de venta.
        valid_states = ['completado', 'pendiente', 'cancelado']
        if estado not in valid_states:  # Verifica si el estado proporcionado es válido.
            raise ValueError("El estado proporcionado no es válido.")
        
        # Verifica que la fecha final no sea anterior a la fecha de inicio.
        if fecha_final < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la fecha de inicio.")
        
        # Crea una nueva instancia de OrdenVenta con los datos proporcionados.
        orden_venta = OrdenVenta(fecha_inicio=fecha_inicio, fecha_final=fecha_final, estado=estado, id_cliente=id_cliente)
        db.session.add(orden_venta)  # Agrega la nueva orden de venta a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return orden_venta  # Retorna la orden de venta creada.

    @staticmethod
    def get_all_ordenes_venta():
        """
        Obtener todas las órdenes de venta de la base de datos.
        
        Returns:
            List[OrdenVenta]: Lista de todas las órdenes de venta.
        """
        # Devuelve todas las órdenes de venta almacenadas en la base de datos.
        return OrdenVenta.query.all()  # Utiliza el método query de SQLAlchemy para obtener todos los registros.

    @staticmethod
    def update_orden_venta(id_orden_venta, new_data):
        """
        Actualizar los datos de una orden de venta existente.
        
        Args:
            id_orden_venta (int): ID de la orden de venta a actualizar.
            new_data (dict): Diccionario con los nuevos datos.
        
        Returns:
            OrdenVenta: La orden de venta actualizada.
        """
        # Busca la orden de venta por su ID en la base de datos.
        orden_venta = OrdenVenta.query.get(id_orden_venta)
        if not orden_venta:  # Si no se encuentra la orden, lanza un error.
            raise ValueError('Orden de venta no encontrada')

        # Verifica que el ID del cliente proporcionado exista si se incluye en new_data.
        if 'id_cliente' in new_data:
            cliente = Cliente.query.get(new_data['id_cliente'])
            if not cliente:  # Si no se encuentra el cliente, lanza un error.
                raise ValueError("El cliente especificado no existe.")
        
        # Verifica que el estado proporcionado sea válido si se incluye en new_data.
        if 'estado' in new_data and new_data['estado'] not in ['completado', 'pendiente', 'cancelado']:
            raise ValueError("El estado proporcionado no es válido.")

        # Verifica que la fecha final no sea anterior a la fecha de inicio si ambas se incluyen en new_data.
        if 'fecha_inicio' in new_data and 'fecha_final' in new_data:
            if new_data['fecha_final'] < new_data['fecha_inicio']:
                raise ValueError("La fecha final no puede ser anterior a la fecha de inicio.")
        
        # Actualiza los atributos de la orden de venta con los nuevos datos proporcionados.
        for key, value in new_data.items():
            if hasattr(orden_venta, key):  # Verifica si la orden tiene el atributo que se quiere actualizar.
                setattr(orden_venta, key, value)  # Actualiza el atributo con el nuevo valor.

        db.session.commit()  # Confirma los cambios en la base de datos.
        return orden_venta  # Retorna la orden de venta actualizada.

    @staticmethod
    def delete_orden_venta(id_orden_venta):
        """
        Eliminar una orden de venta existente.
        
        Args:
            id_orden_venta (int): ID de la orden de venta a eliminar.
        
        Returns:
            None
        """
        # Busca la orden de venta por su ID en la base de datos.
        orden_venta = OrdenVenta.query.get(id_orden_venta)
        if not orden_venta:  # Si no se encuentra la orden, lanza un error.
            raise ValueError('Orden de venta no encontrada')
        
        db.session.delete(orden_venta)  # Elimina la orden de venta de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        
        