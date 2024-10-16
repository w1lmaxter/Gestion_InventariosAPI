from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.cliente_service import ClienteService

# Crear un espacio de nombres (namespace) para los clientes.
# Esto ayuda a organizar las rutas de la API relacionadas con los clientes.
cliente_ns = Namespace('Clientes', description='Operaciones relacionadas con los clientes')

# Definir el modelo de cliente para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se esperan al crear o actualizar un cliente.
cliente_model = cliente_ns.model('Cliente', {
    'nombre': fields.String(required=True, description='Nombre del cliente'),  # Nombre del cliente, requerido.
    'contacto': fields.String(required=True, description='Nombre de contacto'),  # Nombre de contacto, requerido.
    'telefono': fields.String(required=True, description='Teléfono del cliente'),  # Teléfono, requerido.
    'direccion': fields.String(required=True, description='Dirección del cliente'),  # Dirección, requerida.
})

@cliente_ns.route('/')  # Define la ruta base para las operaciones de cliente.
class ClienteResource(Resource):
    
    @cliente_ns.doc('create_cliente')  # Docstring para documentar la operación.
    @cliente_ns.expect(cliente_model, validate=True)  # Espera el modelo definido anteriormente.
    def post(self):
        """
        Crear un nuevo cliente
        ---
        Este método permite crear un nuevo cliente proporcionando su información.
        
        Responses:
        - 201: Cliente creado con éxito.
        - 400: Si ocurre un error durante la creación del cliente.
        """
        # Obtiene los datos del cliente en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear un cliente usando los datos obtenidos.
            cliente = ClienteService.create_cliente(data['nombre'], data['contacto'], data['telefono'], data['direccion'])
            return {'message': 'Cliente creado con éxito', 'cliente': cliente.nombre}, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si falla la creación.

    @cliente_ns.doc('get_clientes')  # Docstring para documentar la operación de obtención.
    def get(self):
        """
        Obtener todos los clientes
        ---
        Este método permite obtener una lista de todos los clientes registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de clientes.
        """
        # Llama al servicio para obtener todos los clientes.
        clientes = ClienteService.get_all_clientes()
        # Devuelve una lista de clientes en formato JSON.
        return {'clientes': [{'id': c.id_cliente, 'nombre': c.nombre, "contacto": c.contacto, "telefono": c.telefono, "direccion": c.direccion} for c in clientes]}, 200

@cliente_ns.route('/<int:id_cliente>')  # Define la ruta para operaciones sobre un cliente específico usando su ID.
@cliente_ns.param('id_cliente', 'El ID del cliente')  # Define el parámetro ID en la documentación.
class ClienteDetailResource(Resource):

    @cliente_ns.doc('update_cliente')  # Docstring para documentar la operación de actualización.
    @cliente_ns.expect(cliente_model, validate=True)  # Espera el modelo definido anteriormente.
    def put(self, id_cliente):
        """
        Actualizar un cliente
        ---
        Este método permite actualizar la información de un cliente basado en su ID.

        Responses:
        - 200: Cliente actualizado con éxito.
        - 404: Si el cliente no se encuentra.
        """
        # Obtiene los nuevos datos del cliente en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar el cliente con el ID especificado y los nuevos datos.
            ClienteService.update_cliente(id_cliente, new_data)
            return {'message': 'Cliente actualizado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Cliente no encontrado'}, 404  # Respuesta de error si no se encuentra el cliente.

    @cliente_ns.doc('delete_cliente')  # Docstring para documentar la operación de eliminación.
    def delete(self, id_cliente):
        """
        Eliminar un cliente
        ---
        Este método permite eliminar un cliente existente basado en su ID.

        Responses:
        - 200: Cliente eliminado con éxito.
        - 404: Si el cliente no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el cliente con el ID especificado.
            ClienteService.delete_cliente(id_cliente)
            return {'message': 'Cliente eliminado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Cliente no encontrado'}, 404  # Respuesta de error si no se encuentra el cliente.