"""
Usuarios, modelos
"""
from flask import current_app
from flask_login import UserMixin

from lib.universal_mixin import UniversalMixin
from turnos.extensions import db, pwd_context
from turnos.blueprints.tareas.models import Tarea


class Usuario(db.Model, UserMixin, UniversalMixin):
    """Usuario"""

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id = db.Column(db.Integer(), primary_key=True)

    # Clave foránea
    autoridad_id = db.Column(db.Integer, db.ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = db.relationship("Autoridad", back_populates="usuarios")

    # Columnas
    email = db.Column(db.String(256), unique=True, index=True)
    contrasena = db.Column(db.String(256), nullable=False)
    nombres = db.Column(db.String(256), nullable=False)
    apellido_paterno = db.Column(db.String(256), nullable=False)
    apellido_materno = db.Column(db.String(256))
    curp = db.Column(db.String(256), unique=True)
    puesto = db.Column(db.String(256))

    # Hijos
    bitacoras = db.relationship("Bitacora", back_populates="usuario", lazy="noload")
    entradas_salidas = db.relationship("EntradaSalida", back_populates="usuario", lazy="noload")
    tareas = db.relationship("Tarea", back_populates="usuario", lazy="noload")
    usuarios_roles = db.relationship("UsuarioRol", back_populates="usuario")

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    @classmethod
    def find_by_identity(cls, identity):
        """Encontrar a un usuario por su correo electrónico"""
        return Usuario.query.filter(Usuario.email == identity).first()

    @property
    def is_active(self):
        """¿Es activo?"""
        return self.estatus == "A"

    def authenticated(self, with_password=True, password=""):
        """Ensure a user is authenticated, and optionally check their password."""
        if self.id and with_password:
            return pwd_context.verify(password, self.contrasena)
        return True

    def can(self, perm):
        """¿Tiene permiso?"""
        return True  # self.rol.has_permission(perm)

    def can_view(self, module):
        """¿Tiene permiso para ver?"""
        return True  # self.rol.can_view(module)

    def can_insert(self, module):
        """¿Tiene permiso para agregar?"""
        return True  # self.rol.can_insert(module)

    def can_edit(self, module):
        """¿Tiene permiso para editar?"""
        return True  # self.rol.can_edit(module)

    def can_admin(self, module):
        """¿Tiene permiso para administrar?"""
        return True  # self.rol.can_admin(module)

    def launch_task(self, nombre, descripcion, *args, **kwargs):
        """Arrancar tarea"""
        rq_job = current_app.task_queue.enqueue("turnos.blueprints." + nombre, *args, **kwargs)
        tarea = Tarea(id=rq_job.get_id(), nombre=nombre, descripcion=descripcion, usuario=self)
        tarea.save()
        return tarea

    def get_tasks_in_progress(self):
        """Obtener tareas"""
        return Tarea.query.filter_by(usuario=self, ha_terminado=False).all()

    def get_task_in_progress(self, nombre):
        """Obtener progreso de una tarea"""
        return Tarea.query.filter_by(nombre=nombre, usuario=self, ha_terminado=False).first()

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.email}>"
