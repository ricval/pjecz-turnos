"""
Usuarios-Roles, formularios
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from turnos.blueprints.roles.models import Rol
from turnos.blueprints.usuarios.models import Usuario


def roles_opciones():
    """Roles: opciones para select"""
    return Rol.query.filter_by(estatus="A").order_by(Rol.nombre).all()


def usuarios_opciones():
    """Usuarios: opciones para select"""
    return Usuario.query.filter_by(estatus="A").order_by(Usuario.email).all()


class UsuarioRolForm(FlaskForm):
    """Formulario UsuarioRol"""

    rol = QuerySelectField(query_factory=roles_opciones, get_label='nombre')
    usuario = QuerySelectField(query_factory=usuarios_opciones, get_label='email')
    guardar = SubmitField("Guardar")
