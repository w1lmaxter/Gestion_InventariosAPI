from flask import request  # Importa la clase request de Flask para manejar las solicitudes HTTP.
from flask_restx import Namespace, Resource, fields  # Importa las herramientas necesarias para crear una API RESTful.
from app.services.orden_venta_service import OrdenVentaService  # Importa el servicio que maneja la lógica de negocio de las órdenes de venta.

# Crear un espacio de nombres (namespace) para las órdenes de venta.
# Esto organiza las rutas relacionadas con las órdenes de venta en la API.
orden_venta_ns = Namespace('Ordenes de venta', description='Operaciones relacionadas con las órdenes de venta')

# Definir el modelo de orden de venta para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se enviarán al crear o actualizar una orden de venta.
orden_venta_model = orden_venta_ns.model('OrdenVenta', {
    'fecha_inicio': fields.Date(required=True, description='Fecha de inicio de la orden'),  # Fecha de inicio, requerida.
    'fecha_final': fields.Date(required=True, description='Fecha final de la orden'),  # Fecha final, requerida.
    'estado': fields.String(required=True, description='Estado de la orden'),  # Estado de la orden, requerido.
    'id_cliente': fields.Integer(required=True, description='ID del cliente asociado'),  # ID del cliente, requerido.
})

@orden_venta_ns.route('/')  # Define la ruta base para las operaciones de órdenes de venta.
class OrdenVentaResource(Resource):
    @orden_venta_ns.doc('create_orden_venta')  # Documenta la operación de creación de la orden de venta.
    @orden_venta_ns.expect(orden_venta_model, validate=True)  # Espera un modelo válido para la creación.
    def post(self):
        """
        Crear una nueva orden de venta
        ---
        Este método permite crear una nueva orden de venta proporcionando su información.
        
        Responses:
        - 201: Orden de venta creada con éxito.
        - 400: Si ocurre un error durante la creación de la orden de venta.
        """
        # Obtiene los datos de la orden de venta en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear una nueva orden de venta con los datos proporcionados.
            orden_venta = OrdenVentaService.create_orden_venta(
                data['fecha_inicio'],
                data['fecha_final'],
                data['estado'],
                data['id_cliente']
            )
            return {
                'message': 'Orden de venta creada con éxito',
                'orden_venta': orden_venta.id_orden_venta  # Retorna el ID de la orden de venta creada.
            }, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si la creación falla.

    @orden_venta_ns.doc('get_ordenes_venta')  # Documenta la operación para obtener todas las órdenes de venta.
    def get(self):
        """
        Obtener todas las órdenes de venta
        ---
        Este método permite obtener una lista de todas las órdenes de venta registradas en la base de datos.

        Responses:
        - 200: Retorna una lista de órdenes de venta.
        """
        # Llama al servicio para obtener todas las órdenes de venta.
        ordenes_venta = OrdenVentaService.get_all_ordenes_venta()
        # Devuelve una lista de órdenes de venta en formato JSON.
        return {
            'ordenes_venta': [{
                'id': o.id_orden_venta,  # ID de la orden de venta.
                'id_cliente': o.id_cliente,  # ID del cliente asociado.
                'fecha_inicio': o.fecha_inicio.strftime('%Y-%m-%d'),  # Fecha de inicio formateada.
                'fecha_final': o.fecha_final.strftime('%Y-%m-%d'),  # Fecha final formateada.
                'estado': o.estado  # Estado de la orden.
            } for o in ordenes_venta]  # Itera sobre todas las órdenes de venta.
        }, 200  # Respuesta exitosa.

@orden_venta_ns.route('/<int:id_orden_venta>')  # Define la ruta para operaciones sobre una orden específica usando su ID.
@orden_venta_ns.param('id_orden_venta', 'El ID de la orden de venta')  # Define el parámetro ID en la documentación.
class OrdenVentaDetailResource(Resource):
    @orden_venta_ns.doc('update_orden_venta')  # Documenta la operación de actualización de la orden de venta.
    @orden_venta_ns.expect(orden_venta_model, validate=True)  # Espera un modelo válido para la actualización.
    def put(self, id_orden_venta):
        """
        Actualizar una orden de venta
        ---
        Este método permite actualizar la información de una orden de venta basada en su ID.

        Responses:
        - 200: Orden de venta actualizada con éxito.
        - 404: Si la orden de venta no se encuentra.
        """
        # Obtiene los nuevos datos de la orden de venta en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar la orden de venta con el ID especificado y los nuevos datos.
            OrdenVentaService.update_orden_venta(id_orden_venta, new_data)
            return {'message': 'Orden de venta actualizada con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Orden de venta no encontrada'}, 404  # Respuesta de error si no se encuentra la orden.

    @orden_venta_ns.doc('delete_orden_venta')  # Documenta la operación de eliminación de la orden de venta.
    def delete(self, id_orden_venta):
        """
        Eliminar una orden de venta
        ---
        Este método permite eliminar una orden de venta existente basada en su ID.

        Responses:
        - 200: Orden de venta eliminada con éxito.
        - 404: Si la orden de venta no se encuentra.
        """
        try:
            # Llama al servicio para eliminar la orden de venta con el ID especificado.
            OrdenVentaService.delete_orden_venta(id_orden_venta)
            return {'message': 'Orden de venta eliminada con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Orden de venta no encontrada'}, 404  # Respuesta de error si no se encuentra la orden.