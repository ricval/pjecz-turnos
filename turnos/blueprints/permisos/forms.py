"""
Permisos, formularios
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

NIVELES = [
    (0, "NULO"),
    (1, "VER"),
    (2, "VER y MODIFICAR"),
    (3, "VER, MODIFICAR y CREAR"),
    (4, "ADMINISTRAR"),
]


class PermisoForm(FlaskForm):
    """ Formulario Permiso """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=256)])
    nivel = SelectField('Nivel', validators=[DataRequired()], choices=NIVELES, coerce=int)
    guardar = SubmitField('Guardar')
