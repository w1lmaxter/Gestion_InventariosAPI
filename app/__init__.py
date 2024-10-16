from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_migrate import Migrate
from .config import Config

# Inicializamos las extensiones globalmente para luego asociarlas a la app en la función create_app
db = SQLAlchemy()
migrate = Migrate()  # Para gestionar las migraciones de la base de datos
bcrypt = Bcrypt()
jwt = JWTManager()  # Para la gestión de tokens JWT en la autenticación

def create_app():
    app = Flask(__name__)

    # Configuraciones de la aplicación
    app.config.from_object(Config)  # Cargar la configuración

    # Inicializamos las extensiones con la aplicación
    db.init_app(app)  # Inicializar SQLAlchemy con la app
    bcrypt.init_app(app)  # Inicializar Bcrypt con la app
    jwt.init_app(app)  # Inicializar JWTManager con la app
    migrate.init_app(app, db)  # Inicializar Migrate con la app y la base de datos

    authorizations = {
        "Bearer": {
            "type": "apiKey",  # Tipo apiKey define que el token JWT se envía en el encabezado de la solicitud
            "in": "header",  # El token JWT se debe enviar en el encabezado de la solicitud HTTP
            "name": "Authorization",  # Nombre del campo del encabezado HTTP para el token
            "description": 'JWT Bearer token. Ejemplo: "Bearer {token}"',  # Instrucción sobre cómo enviar el token
        }
    }

    # URL de la imagen que quieres mostrar (sustituye por la URL real)
    image_url = "https://nbxsoluciones.com/wp-content/uploads/2022/06/api_portada.jpg"  

    # Configuramos la API Flask-RESTX
    api = Api(
        app,  # La aplicación Flask en la que registramos la API
        title="API de Gestión de Inventarios",  # Título de la API
        version="1.0",  # Versión de la API
        description=f'<img src="{image_url}" alt="Imagen de gestión de inventarios" width="800" height="300"><br>API para gestión de productos',  # Aumentar tamaño de la imagen
        authorizations=authorizations,  # Añadimos la configuración de JWT a la API
        security="Bearer",  # Define que los endpoints por defecto usan el esquema de seguridad JWT
    )

    # Importar y registrar los namespaces de los controladores
    from app.controllers.proveedor_controller import proveedor_ns
    from app.controllers.cliente_controller import cliente_ns
    from app.controllers.producto_controller import producto_ns
    from app.controllers.detalle_orden_venta_controller import detalle_orden_venta_ns
    from app.controllers.detalle_orden_compra_controller import detalle_orden_compra_ns
    from app.controllers.orden_compra_controller import orden_compra_ns
    from app.controllers.orden_venta_controller import orden_venta_ns

    api.add_namespace(proveedor_ns)
    api.add_namespace(cliente_ns)
    api.add_namespace(producto_ns)
    api.add_namespace(detalle_orden_venta_ns)
    api.add_namespace(detalle_orden_compra_ns)
    api.add_namespace(orden_compra_ns)  # Agrega el namespace de órdenes de compra
    api.add_namespace(orden_venta_ns)

    return app