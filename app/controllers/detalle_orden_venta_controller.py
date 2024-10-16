from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.detalle_orden_venta_service import DetalleOrdenVentaService

# Crear un espacio de nombres (namespace) para los detalles de las órdenes de venta.
# Esto organiza las rutas de la API que están relacionadas con los detalles de las órdenes de venta.
detalle_orden_venta_ns = Namespace("Detalles de ordenes de venta",
    description="Operaciones relacionadas con los detalles de órdenes de venta",
)

# Definir el modelo de detalle de orden de venta para la documentación de Swagger.
# Este modelo describe cómo deben lucir los datos para crear o actualizar un detalle de orden de venta.
detalle_model = detalle_orden_venta_ns.model(
    "DetalleOrdenVenta",
    {
        "id_orden_venta": fields.Integer(
            required=True, description="ID de la orden de venta"  # ID de la orden de venta, requerido.
        ),
        "id_producto": fields.Integer(required=True, description="ID del producto"),  # ID del producto, requerido.
        "cantidad": fields.Integer(required=True, description="Cantidad del producto"),  # Cantidad del producto, requerida.
    },
)

@detalle_orden_venta_ns.route("/")  # Define la ruta base para las operaciones de detalle de orden de venta.
class DetalleOrdenVentaResource(Resource):
    
    @detalle_orden_venta_ns.doc("create_detalle_orden_venta")  # Docstring para documentar la operación de creación.
    @detalle_orden_venta_ns.expect(detalle_model, validate=True)  # Espera el modelo definido anteriormente.
    def post(self):
        """
        Crear un nuevo detalle de orden de venta
        ---
        Este método permite crear un nuevo detalle de orden de venta proporcionando su información.

        Responses:
        - 201: Detalle de orden de venta creado con éxito.
        - 400: Si ocurre un error durante la creación del detalle de orden de venta.
        """
        # Obtiene los datos del detalle de orden de venta en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear un detalle de orden de venta usando los datos obtenidos.
            detalle = DetalleOrdenVentaService.create_detalle_orden_venta(
                data["id_orden_venta"], data["id_producto"], data["cantidad"]
            )
            return {
                "message": "Detalle de orden de venta creado con éxito",
                "detalle": detalle.id_detalle_venta,
            }, 201  # Respuesta exitosa con el ID del detalle creado.
        except ValueError as e:
            return {"message": str(e)}, 400  # Respuesta de error si falla la creación.

    @detalle_orden_venta_ns.doc("get_all_detalles_orden_venta")  # Docstring para documentar la operación de obtención.
    def get(self):
        """
        Obtener todos los detalles de orden de venta
        ---
        Este método permite obtener todos los detalles de orden de venta.

        Responses:
        - 200: Retorna una lista de todos los detalles de orden de venta.
        """
        # Llama al servicio para obtener todos los detalles de órdenes de venta.
        detalles = DetalleOrdenVentaService.get_all_detalles_orden_venta()
        # Devuelve una lista de detalles en formato JSON.
        return {
            "detalles_orden_venta": [
                {
                    "id": d.id_detalle_venta,  # ID del detalle de venta.
                    "id_orden_venta": d.id_orden_venta,  # ID de la orden de venta asociada.
                    "id_producto": d.id_producto,  # ID del producto asociado.
                    "cantidad": d.cantidad,  # Cantidad del producto.
                }
                for d in detalles  # Itera sobre todos los detalles obtenidos.
            ]
        }, 200  # Respuesta exitosa con la lista de detalles.

@detalle_orden_venta_ns.route("/<int:id_detalle>")  # Define la ruta para operaciones sobre un detalle específico usando su ID.
@detalle_orden_venta_ns.param("id_detalle", "El ID del detalle de orden de venta")  # Define el parámetro ID en la documentación.
class DetalleOrdenVentaDetailResource(Resource):
    
    @detalle_orden_venta_ns.doc('update_detalle_orden_venta')  # Docstring para documentar la operación de actualización.
    @detalle_orden_venta_ns.expect(detalle_model, validate=True)  # Espera el modelo definido anteriormente.
    def put(self, id_detalle):
        """
        Actualizar un detalle de orden de venta
        ---
        Este método permite actualizar la información de un detalle de orden de venta basado en su ID.

        Responses:
        - 200: Detalle de orden de venta actualizado con éxito.
        - 404: Si el detalle de orden de venta no se encuentra.
        """
        # Obtiene los nuevos datos del detalle de orden de venta en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar el detalle de orden de venta con el ID especificado y los nuevos datos.
            detalle = DetalleOrdenVentaService.update_detalle_orden_venta(id_detalle, new_data)
            return {
                'message': 'Detalle de orden de venta actualizado con éxito',
                'detalle': detalle.id_detalle_venta
            }, 200  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 404  # Respuesta de error si no se encuentra el detalle.

    @detalle_orden_venta_ns.doc("delete_detalle_orden_venta")  # Docstring para documentar la operación de eliminación.
    def delete(self, id_detalle):
        """
        Eliminar un detalle de orden de venta
        ---
        Este método permite eliminar un detalle de orden de venta existente basado en su ID.

        Responses:
        - 200: Detalle de orden de venta eliminado con éxito.
        - 404: Si el detalle de orden de venta no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el detalle de orden de venta con el ID especificado.
            DetalleOrdenVentaService.delete_detalle_orden_venta(id_detalle)
            return {"message": "Detalle de orden de venta eliminado con éxito"}, 200  # Respuesta exitosa.
        except ValueError as e:
            return {"message": str(e)}, 404  # Respuesta de error si no se encuentra el detalle.