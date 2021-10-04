"""
Permisos, formularios
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.roles.models import Rol

NIVELES = [
    (0, "NULO"),
    (1, "VER"),
    (2, "VER y MODIFICAR"),
    (3, "VER, MODIFICAR y CREAR"),
    (4, "ADMINISTRAR"),
]


def modulos_opciones():
    """ Modulos: opciones para select """
    return Modulo.query.filter_by(estatus='A').order_by(Modulo.nombre).all()


def roles_opciones():
    """ Roles: opciones para select """
    return Rol.query.filter_by(estatus='A').order_by(Rol.nombre).all()


class PermisoForm(FlaskForm):
    """ Formulario Permiso """
    modulo = QuerySelectField(query_factory=modulos_opciones, get_label='nombre')
    rol = QuerySelectField(query_factory=roles_opciones, get_label='nombre')
    nivel = SelectField('Nivel', validators=[DataRequired()], choices=NIVELES, coerce=int)
    guardar = SubmitField('Guardar')
