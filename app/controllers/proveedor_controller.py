from flask import request  # Importa la clase request de Flask para manejar las solicitudes HTTP.
from flask_restx import Namespace, Resource, fields  # Importa las herramientas necesarias para crear una API RESTful.
from app.services.proveedor_service import ProveedorService  # Importa el servicio que maneja la lógica de negocio de los proveedores.

# Crear un espacio de nombres (namespace) para los proveedores.
# Esto organiza las rutas relacionadas con los proveedores en la API.
proveedor_ns = Namespace('Proveedores', description='Operaciones relacionadas con los proveedores')

# Definir el modelo de proveedor para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se enviarán al crear o actualizar un proveedor.
proveedor_model = proveedor_ns.model('Proveedor', {
    'nombre': fields.String(required=True, description='Nombre del proveedor'),  # Nombre del proveedor, requerido.
    'contacto': fields.String(required=True, description='Nombre de contacto'),  # Nombre de contacto, requerido.
    'telefono': fields.String(required=True, description='Teléfono del proveedor'),  # Teléfono del proveedor, requerido.
    'direccion': fields.String(required=True, description='Dirección del proveedor'),  # Dirección del proveedor, requerido.
})

@proveedor_ns.route('/')  # Define la ruta base para las operaciones de proveedores.
class ProveedorResource(Resource):
    @proveedor_ns.doc('create_proveedor')  # Documenta la operación de creación del proveedor.
    @proveedor_ns.expect(proveedor_model, validate=True)  # Espera un modelo válido para la creación.
    def post(self):
        """
        Crear un nuevo proveedor
        ---
        Este método permite crear un nuevo proveedor proporcionando su información.
        
        Responses:
        - 201: Proveedor creado con éxito.
        - 400: Si ocurre un error durante la creación del proveedor.
        """
        # Obtiene los datos del proveedor en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear un nuevo proveedor con los datos proporcionados.
            proveedor = ProveedorService.create_proveedor(data['nombre'], data['contacto'], data['telefono'], data['direccion'])
            return {
                'message': 'Proveedor creado con éxito',
                'proveedor': proveedor.nombre  # Retorna el nombre del proveedor creado.
            }, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si la creación falla.

    @proveedor_ns.doc('get_proveedores')  # Documenta la operación para obtener todos los proveedores.
    def get(self):
        """
        Obtener todos los proveedores
        ---
        Este método permite obtener una lista de todos los proveedores registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de proveedores.
        """
        # Llama al servicio para obtener todos los proveedores.
        proveedores = ProveedorService.get_all_proveedores()
        # Devuelve una lista de proveedores en formato JSON.
        return {
            'proveedores': [
                {
                    'id_proveedor': p.id_proveedor,  # ID del proveedor.
                    'nombre': p.nombre,  # Nombre del proveedor.
                    'contacto': p.contacto,  # Nombre de contacto.
                    'telefono': p.telefono,  # Teléfono del proveedor.
                    'direccion': p.direccion  # Dirección del proveedor.
                } for p in proveedores  # Itera sobre todos los proveedores.
            ]
        }, 200  # Respuesta exitosa.

@proveedor_ns.route('/<int:id_proveedor>')  # Define la ruta para operaciones sobre un proveedor específico usando su ID.
@proveedor_ns.param('id_proveedor', 'El ID del proveedor')  # Define el parámetro ID en la documentación.
class ProveedorDetailResource(Resource):
    @proveedor_ns.doc('update_proveedor')  # Documenta la operación de actualización del proveedor.
    @proveedor_ns.expect(proveedor_model, validate=True)  # Espera un modelo válido para la actualización.
    def put(self, id_proveedor):
        """
        Actualizar un proveedor
        ---
        Este método permite actualizar la información de un proveedor basado en su ID.

        Responses:
        - 200: Proveedor actualizado con éxito.
        - 404: Si el proveedor no se encuentra.
        """
        # Obtiene los nuevos datos del proveedor en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar el proveedor con el ID especificado y los nuevos datos.
            ProveedorService.update_proveedor(id_proveedor, new_data)
            return {'message': 'Proveedor actualizado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Proveedor no encontrado'}, 404  # Respuesta de error si no se encuentra el proveedor.

    @proveedor_ns.doc('delete_proveedor')  # Documenta la operación de eliminación del proveedor.
    def delete(self, id_proveedor):
        """
        Eliminar un proveedor
        ---
        Este método permite eliminar un proveedor existente basado en su ID.

        Responses:
        - 200: Proveedor eliminado con éxito.
        - 404: Si el proveedor no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el proveedor con el ID especificado.
            ProveedorService.delete_proveedor(id_proveedor)
            return {'message': 'Proveedor eliminado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Proveedor no encontrado'}, 404  # Respuesta de error si no se encuentra el proveedor.