from app import db  # Importa la instancia de la base de datos desde la aplicación.
from app.models.ordenCompra import OrdenCompra  # Importa el modelo OrdenCompra.
from app.models.proveedor import Proveedor  # Importa el modelo Proveedor.

class OrdenCompraService:
    @staticmethod
    def create_orden_compra(fecha_inicio, fecha_final, estado, id_proveedor):
        """
        Crear una nueva orden de compra.
        
        Args:
            fecha_inicio (date): Fecha de inicio de la orden.
            fecha_final (date): Fecha final de la orden.
            estado (str): Estado de la orden.
            id_proveedor (int): ID del proveedor asociado a la orden.
        
        Returns:
            OrdenCompra: La orden de compra creada.
        """
        # Verifica que todos los campos requeridos estén presentes.
        if not all([fecha_inicio, fecha_final, estado, id_proveedor]):
            raise ValueError("Todos los campos son obligatorios.")
        
        # Busca el proveedor por su ID.
        proveedor = Proveedor.query.get(id_proveedor)
        if not proveedor:  # Si no se encuentra el proveedor, lanza un error.
            raise ValueError("El proveedor especificado no existe.")
        
        # Lista de estados válidos para la orden de compra.
        valid_states = ['completado', 'pendiente', 'cancelado']
        if estado not in valid_states:  # Verifica si el estado proporcionado es válido.
            raise ValueError("El estado proporcionado no es válido.")
        
        # Verifica que la fecha final no sea anterior a la fecha de inicio.
        if fecha_final < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la fecha de inicio.")
        
        # Crea una nueva instancia de OrdenCompra con los datos proporcionados.
        orden_compra = OrdenCompra(fecha_inicio=fecha_inicio, fecha_final=fecha_final, estado=estado, id_proveedor=id_proveedor)
        db.session.add(orden_compra)  # Agrega la nueva orden de compra a la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return orden_compra  # Retorna la orden de compra creada.

    @staticmethod
    def get_all_ordenes_compra():
        """
        Obtener todas las órdenes de compra de la base de datos.
        
        Returns:
            List[OrdenCompra]: Lista de todas las órdenes de compra.
        """
        # Devuelve todas las órdenes de compra almacenadas en la base de datos.
        return OrdenCompra.query.all()  # Utiliza el método query de SQLAlchemy para obtener todos los registros.

    @staticmethod
    def update_orden_compra(id_orden_compra, new_data):
        """
        Actualizar los datos de una orden de compra existente.
        
        Args:
            id_orden_compra (int): ID de la orden de compra a actualizar.
            new_data (dict): Diccionario con los nuevos datos.
        
        Returns:
            OrdenCompra: La orden de compra actualizada.
        """
        # Busca la orden de compra por su ID en la base de datos.
        orden_compra = OrdenCompra.query.get(id_orden_compra)
        if not orden_compra:  # Si no se encuentra la orden, lanza un error.
            raise ValueError('Orden de compra no encontrada')

        # Verifica que el ID del proveedor proporcionado exista si se incluye en new_data.
        if 'id_proveedor' in new_data:
            proveedor = Proveedor.query.get(new_data['id_proveedor'])
            if not proveedor:  # Si no se encuentra el proveedor, lanza un error.
                raise ValueError("El proveedor especificado no existe.")

        # Verifica que el estado proporcionado sea válido si se incluye en new_data.
        if 'estado' in new_data and new_data['estado'] not in ['completado', 'pendiente', 'cancelado']:
            raise ValueError("El estado proporcionado no es válido.")

        # Verifica que la fecha final no sea anterior a la fecha de inicio si ambas se incluyen en new_data.
        if 'fecha_inicio' in new_data and 'fecha_final' in new_data:
            if new_data['fecha_final'] < new_data['fecha_inicio']:
                raise ValueError("La fecha final no puede ser anterior a la fecha de inicio.")
        
        # Actualiza los atributos de la orden de compra con los nuevos datos proporcionados.
        for key, value in new_data.items():
            if hasattr(orden_compra, key):  # Verifica si la orden tiene el atributo que se quiere actualizar.
                setattr(orden_compra, key, value)  # Actualiza el atributo con el nuevo valor.

        db.session.commit()  # Confirma los cambios en la base de datos.
        return orden_compra  # Retorna la orden de compra actualizada.

    @staticmethod
    def delete_orden_compra(id_orden_compra):
        """
        Eliminar una orden de compra existente.
        
        Args:
            id_orden_compra (int): ID de la orden de compra a eliminar.
        
        Returns:
            None
        """
        # Busca la orden de compra por su ID en la base de datos.
        orden_compra = OrdenCompra.query.get(id_orden_compra)
        if not orden_compra:  # Si no se encuentra la orden, lanza un error.
            raise ValueError('Orden de compra no encontrada')
        
        db.session.delete(orden_compra)  # Elimina la orden de compra de la sesión de la base de datos.
        db.session.commit()  # Confirma los cambios en la base de datos.