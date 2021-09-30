"""
Flask App
"""
from flask import Flask
from redis import Redis
import rq

from turnos.extensions import csrf, db, login_manager, moment

from turnos.blueprints.autoridades.views import autoridades
from turnos.blueprints.bitacoras.views import bitacoras
from turnos.blueprints.distritos.views import distritos
from turnos.blueprints.entradas_salidas.views import entradas_salidas
from turnos.blueprints.modulos.views import modulos
from turnos.blueprints.permisos.views import permisos
from turnos.blueprints.roles.views import roles
from turnos.blueprints.sistemas.views import sistemas
from turnos.blueprints.tareas.views import tareas
from turnos.blueprints.usuarios.views import usuarios
from turnos.blueprints.usuarios_roles.views import usuarios_roles

from turnos.blueprints.usuarios.models import Usuario


def create_app():
    """Crear app"""
    # Definir app
    app = Flask(__name__, instance_relative_config=True)
    # Cargar la configuración para producción en config/settings.py
    app.config.from_object("config.settings")
    # Cargar la configuración para desarrollo en instance/settings.py
    app.config.from_pyfile("settings.py", silent=True)
    # Redis
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue(app.config["TASK_QUEUE"], connection=app.redis, default_timeout=1920)
    # Cargar los blueprints
    app.register_blueprint(autoridades)
    app.register_blueprint(bitacoras)
    app.register_blueprint(distritos)
    app.register_blueprint(entradas_salidas)
    app.register_blueprint(modulos)
    app.register_blueprint(permisos)
    app.register_blueprint(roles)
    app.register_blueprint(sistemas)
    app.register_blueprint(tareas)
    app.register_blueprint(usuarios)
    app.register_blueprint(usuarios_roles)
    # Cargar las extensiones
    extensions(app)
    authentication(Usuario)
    # Entregar app
    return app


def extensions(app):
    """Incorporar las extensiones"""
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)


def authentication(user_model):
    """Inicializar Flask-Login"""
    login_manager.login_view = "usuarios.login"

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)
