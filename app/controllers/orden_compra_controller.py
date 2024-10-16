from flask import request  # Importa la clase request de Flask para manejar las solicitudes HTTP.
from flask_restx import Namespace, Resource, fields  # Importa las herramientas necesarias para crear una API RESTful.
from app.services.orden_compra_service import OrdenCompraService  # Importa el servicio que maneja la lógica de negocio de las órdenes de compra.

# Crear un espacio de nombres (namespace) para las órdenes de compra.
# Esto ayuda a organizar las rutas relacionadas con las órdenes de compra en la API.
orden_compra_ns = Namespace('Ordenes de compra', description='Operaciones relacionadas con las órdenes de compra')

# Definir el modelo de orden de compra para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se enviarán al crear o actualizar una orden de compra.
orden_compra_model = orden_compra_ns.model('OrdenCompra', {
    'fecha_inicio': fields.Date(required=True, description='Fecha de inicio de la orden'),  # Fecha de inicio, requerida.
    'fecha_final': fields.Date(required=True, description='Fecha final de la orden'),  # Fecha final, requerida.
    'estado': fields.String(required=True, description='Estado de la orden'),  # Estado de la orden, requerido.
    'id_proveedor': fields.Integer(required=True, description='ID del proveedor asociado'),  # ID del proveedor, requerido.
})

@orden_compra_ns.route('/')  # Define la ruta base para las operaciones de órdenes de compra.
class OrdenCompraResource(Resource):
    @orden_compra_ns.doc('create_orden_compra')  # Documenta la operación de creación de la orden de compra.
    @orden_compra_ns.expect(orden_compra_model, validate=True)  # Espera un modelo válido para la creación.
    def post(self):
        """
        Crear una nueva orden de compra
        ---
        Este método permite crear una nueva orden de compra proporcionando su información.
        
        Responses:
        - 201: Orden de compra creada con éxito.
        - 400: Si ocurre un error durante la creación de la orden de compra.
        """
        # Obtiene los datos de la orden de compra en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear una nueva orden de compra con los datos proporcionados.
            orden_compra = OrdenCompraService.create_orden_compra(
                data['fecha_inicio'],
                data['fecha_final'],
                data['estado'],
                data['id_proveedor']
            )
            return {
                'message': 'Orden de compra creada con éxito',
                'orden_compra': orden_compra.id_orden_compra  # Retorna el ID de la orden de compra creada.
            }, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si la creación falla.

    @orden_compra_ns.doc('get_ordenes_compra')  # Documenta la operación para obtener todas las órdenes de compra.
    def get(self):
        """
        Obtener todas las órdenes de compra
        ---
        Este método permite obtener una lista de todas las órdenes de compra registradas en la base de datos.

        Responses:
        - 200: Retorna una lista de órdenes de compra.
        """
        # Llama al servicio para obtener todas las órdenes de compra.
        ordenes_compra = OrdenCompraService.get_all_ordenes_compra()
        # Devuelve una lista de órdenes de compra en formato JSON.
        return {
            'ordenes_compra': [{
                'id': o.id_orden_compra,  # ID de la orden de compra.
                'id_proveedor': o.id_proveedor,  # ID del proveedor asociado.
                'fecha_inicio': o.fecha_inicio.strftime('%Y-%m-%d'),  # Fecha de inicio formateada.
                'fecha_final': o.fecha_final.strftime('%Y-%m-%d'),  # Fecha final formateada.
                'estado': o.estado  # Estado de la orden.
            } for o in ordenes_compra]  # Itera sobre todas las órdenes de compra.
        }, 200  # Respuesta exitosa.

@orden_compra_ns.route('/<int:id_orden_compra>')  # Define la ruta para operaciones sobre una orden específica usando su ID.
@orden_compra_ns.param('id_orden_compra', 'El ID de la orden de compra')  # Define el parámetro ID en la documentación.
class OrdenCompraDetailResource(Resource):
    @orden_compra_ns.doc('update_orden_compra')  # Documenta la operación de actualización de la orden de compra.
    @orden_compra_ns.expect(orden_compra_model, validate=True)  # Espera un modelo válido para la actualización.
    def put(self, id_orden_compra):
        """
        Actualizar una orden de compra
        ---
        Este método permite actualizar la información de una orden de compra basada en su ID.

        Responses:
        - 200: Orden de compra actualizada con éxito.
        - 404: Si la orden de compra no se encuentra.
        """
        # Obtiene los nuevos datos de la orden de compra en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar la orden de compra con el ID especificado y los nuevos datos.
            OrdenCompraService.update_orden_compra(id_orden_compra, new_data)
            return {'message': 'Orden de compra actualizada con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Orden de compra no encontrada'}, 404  # Respuesta de error si no se encuentra la orden.

    @orden_compra_ns.doc('delete_orden_compra')  # Documenta la operación de eliminación de la orden de compra.
    def delete(self, id_orden_compra):
        """
        Eliminar una orden de compra
        ---
        Este método permite eliminar una orden de compra existente basada en su ID.

        Responses:
        - 200: Orden de compra eliminada con éxito.
        - 404: Si la orden de compra no se encuentra.
        """
        try:
            # Llama al servicio para eliminar la orden de compra con el ID especificado.
            OrdenCompraService.delete_orden_compra(id_orden_compra)
            return {'message': 'Orden de compra eliminada con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Orden de compra no encontrada'}, 404  # Respuesta de error si no se encuentra la orden.