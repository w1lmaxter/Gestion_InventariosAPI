from flask import request  # Importa la clase request de Flask para manejar las solicitudes HTTP.
from flask_restx import Namespace, Resource, fields  # Importa las herramientas necesarias para crear una API RESTful.
from app.services.producto_service import ProductoService  # Importa el servicio que maneja la lógica de negocio de los productos.

# Crear un espacio de nombres (namespace) para los productos.
# Esto organiza las rutas relacionadas con los productos en la API.
producto_ns = Namespace('Productos', description='Operaciones relacionadas con los productos')

# Definir el modelo de producto para la documentación de Swagger.
# Este modelo describe la estructura de los datos que se enviarán al crear o actualizar un producto.
producto_model = producto_ns.model('Producto', {
    'nombre': fields.String(required=True, description='Nombre del producto'),  # Nombre del producto, requerido.
    'costo': fields.Float(required=True, description='Costo del producto'),  # Costo del producto, requerido.
    'precio_venta': fields.Float(required=True, description='Precio de venta del producto'),  # Precio de venta, requerido.
    'cantidad': fields.Integer(required=True, description='Cantidad disponible del producto'),  # Cantidad disponible, requerido.
})

@producto_ns.route('/')  # Define la ruta base para las operaciones de productos.
class ProductoResource(Resource):
    @producto_ns.doc('create_producto')  # Documenta la operación de creación del producto.
    @producto_ns.expect(producto_model, validate=True)  # Espera un modelo válido para la creación.
    def post(self):
        """
        Crear un nuevo producto
        ---
        Este método permite crear un nuevo producto proporcionando su información.
        
        Responses:
        - 201: Producto creado con éxito.
        - 400: Si ocurre un error durante la creación del producto.
        """
        # Obtiene los datos del producto en formato JSON del cuerpo de la solicitud.
        data = request.get_json()
        try:
            # Llama al servicio para crear un nuevo producto con los datos proporcionados.
            producto = ProductoService.create_producto(data['nombre'], data['costo'], data['precio_venta'], data['cantidad'])
            return {
                'message': 'Producto creado con éxito',
                'producto': producto.nombre  # Retorna el nombre del producto creado.
            }, 201  # Respuesta exitosa.
        except ValueError as e:
            return {'message': str(e)}, 400  # Respuesta de error si la creación falla.

    @producto_ns.doc('get_productos')  # Documenta la operación para obtener todos los productos.
    def get(self):
        """
        Obtener todos los productos
        ---
        Este método permite obtener una lista de todos los productos registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de productos.
        """
        # Llama al servicio para obtener todos los productos.
        productos = ProductoService.get_all_productos()
        # Devuelve una lista de productos en formato JSON.
        return {
            'productos': [
                {
                    'id_producto': p.id_producto,  # ID del producto.
                    'nombre': p.nombre,  # Nombre del producto.
                    'costo': float(p.costo),  # Convertir Decimal a float.
                    'precio_venta': float(p.precio_venta),  # Convertir Decimal a float.
                    'cantidad': p.cantidad  # Cantidad disponible.
                } for p in productos  # Itera sobre todos los productos.
            ]
        }, 200  # Respuesta exitosa.

@producto_ns.route('/<int:id_producto>')  # Define la ruta para operaciones sobre un producto específico usando su ID.
@producto_ns.param('id_producto', 'El ID del producto')  # Define el parámetro ID en la documentación.
class ProductoDetailResource(Resource):
    @producto_ns.doc('update_producto')  # Documenta la operación de actualización del producto.
    @producto_ns.expect(producto_model, validate=True)  # Espera un modelo válido para la actualización.
    def put(self, id_producto):
        """
        Actualizar un producto
        ---
        Este método permite actualizar la información de un producto basado en su ID.

        Responses:
        - 200: Producto actualizado con éxito.
        - 404: Si el producto no se encuentra.
        """
        # Obtiene los nuevos datos del producto en formato JSON del cuerpo de la solicitud.
        new_data = request.get_json()
        try:
            # Llama al servicio para actualizar el producto con el ID especificado y los nuevos datos.
            ProductoService.update_producto(id_producto, new_data)
            return {'message': 'Producto actualizado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Producto no encontrado'}, 404  # Respuesta de error si no se encuentra el producto.

    @producto_ns.doc('delete_producto')  # Documenta la operación de eliminación del producto.
    def delete(self, id_producto):
        """
        Eliminar un producto
        ---
        Este método permite eliminar un producto existente basado en su ID.

        Responses:
        - 200: Producto eliminado con éxito.
        - 404: Si el producto no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el producto con el ID especificado.
            ProductoService.delete_producto(id_producto)
            return {'message': 'Producto eliminado con éxito'}, 200  # Respuesta exitosa.
        except ValueError:
            return {'message': 'Producto no encontrado'}, 404  # Respuesta de error si no se encuentra el producto.