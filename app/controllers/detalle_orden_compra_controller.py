from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.detalle_orden_compra_service import DetalleOrdenCompraService

# Crear un espacio de nombres (namespace) para los detalles de las órdenes de compra.
# Esto ayuda a organizar las rutas de la API relacionadas con los detalles de las órdenes de compra.
detalle_orden_compra_ns = Namespace('Detalles de ordenes de compra', description='Operaciones relacionadas con los detalles de órdenes de compra')

# Definir el modelo de detalle de orden de compra para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se esperan al crear o actualizar un detalle de orden de compra.
detalle_model = detalle_orden_compra_ns.model('DetalleOrdenCompra', {
    'id_orden_compra': fields.Integer(required=True, description='ID de la orden de compra'),  # ID de la orden de compra, requerido.
    'id_producto': fields.Integer(required=True, description='ID del producto'),  # ID del producto, requerido.
    'cantidad': fields.Integer(required=True, description='Cantidad del producto'),  # Cantidad del producto, requerida.
})

@detalle_orden_compra_ns.route('/')  # Define la ruta base para las operaciones de detalle de orden de compra.
class DetalleOrdenCompraResource(Resource):
    
    @detalle_orden_compra_ns.doc('create_detalle_orden_compra')  # Docstring para documentar la operación de creación.
    @detalle_orden_compra_ns.expect(detalle_model, validate=True)  # Espera el modelo definido anteriormente.
    def post(self):
        """
        Crear un nuevo detalle de orden de compra
        ---
        Este método permite crear un nuevo detalle de orden de compra proporcionando su información.
        
        Responses:
        - 201: Detalle de orden de compra creado con éxito.
        - 400: Si ocurre un error durante la creación del detalle de orden de compra.
        """
        # Obtiene los datos del detalle de orden de compra en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear un detalle de orden de compra usando los datos obtenidos.
            detalle = DetalleOrdenCompraService.create_detalle_orden_compra(
                data['id_orden_compra'],
                data['id_producto'],
                data['cantidad']
            )
            return {'message': 'Detalle de orden de compra creado con éxito', 'detalle': detalle.id_detalle_compra}, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si falla la creación.

    @detalle_orden_compra_ns.doc('get_all_detalles_orden_compra')  # Docstring para documentar la operación de obtención.
    def get(self):
        """
        Obtener todos los detalles de orden de compra
        ---
        Este método permite obtener todos los detalles de orden de compra.

        Responses:
        - 200: Retorna una lista de todos los detalles de orden de compra.
        """
        # Llama al servicio para obtener todos los detalles de órdenes de compra.
        detalles = DetalleOrdenCompraService.get_all_detalles_orden_compra()
        # Devuelve una lista de detalles en formato JSON.
        return {
            'detalles_orden_compra': [{
                'id': d.id_detalle_compra,
                'id_orden_compra': d.id_orden_compra,
                'id_producto': d.id_producto,
                'cantidad': d.cantidad
            } for d in detalles]
        }, 200

@detalle_orden_compra_ns.route('/<int:id_detalle>')  # Define la ruta para operaciones sobre un detalle específico usando su ID.
@detalle_orden_compra_ns.param('id_detalle', 'El ID del detalle de orden de compra')  # Define el parámetro ID en la documentación.
class DetalleOrdenCompraDetailResource(Resource):

    @detalle_orden_compra_ns.doc('update_detalle_orden_compra')  # Docstring para documentar la operación de actualización.
    @detalle_orden_compra_ns.expect(detalle_model, validate=True)  # Espera el modelo definido anteriormente.
    def put(self, id_detalle):
        """
        Actualizar un detalle de orden de compra
        ---
        Este método permite actualizar la información de un detalle de orden de compra basado en su ID.

        Responses:
        - 200: Detalle de orden de compra actualizado con éxito.
        - 404: Si el detalle de orden de compra no se encuentra.
        """
        # Obtiene los nuevos datos del detalle de orden de compra en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar el detalle de orden de compra con el ID especificado y los nuevos datos.
            detalle = DetalleOrdenCompraService.update_detalle_orden_compra(
                id_detalle,
                new_data['id_producto'],
                new_data['cantidad']
            )
            return {'message': 'Detalle de orden de compra actualizado con éxito', 'detalle': detalle.id_detalle_compra}, 200  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 404  # Respuesta de error si no se encuentra el detalle.

    @detalle_orden_compra_ns.doc('delete_detalle_orden_compra')  # Docstring para documentar la operación de eliminación.
    def delete(self, id_detalle):
        """
        Eliminar un detalle de orden de compra
        ---
        Este método permite eliminar un detalle de orden de compra existente basado en su ID.

        Responses:
        - 200: Detalle de orden de compra eliminado con éxito.
        - 404: Si el detalle de orden de compra no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el detalle de orden de compra con el ID especificado.
            DetalleOrdenCompraService.delete_detalle_orden_compra(id_detalle)
            return {'message': 'Detalle de orden de compra eliminado con éxito'}, 200  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 404  # Respuesta de error si no se encuentra el detalle.