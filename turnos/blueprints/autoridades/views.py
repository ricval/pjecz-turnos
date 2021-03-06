"""
Autoridades, vistas
"""
from flask import Blueprint, render_template
from flask_login import login_required

from turnos.blueprints.autoridades.models import Autoridad
from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required

MODULO = "AUTORIDADES"

autoridades = Blueprint("autoridades", __name__, template_folder="templates")


@autoridades.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@autoridades.route("/autoridades")
def list_active():
    """Listado de Autoridades activos"""
    return render_template(
        "autoridades/list.jinja2",
        autoridades=Autoridad.query.filter(Autoridad.estatus == "A").all(),
        titulo="Autoridades",
        estatus="A",
    )


@autoridades.route("/autoridades/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Autoridades inactivos"""
    return render_template(
        "autoridades/list.jinja2",
        autoridades=Autoridad.query.filter(Autoridad.estatus == "B").all(),
        titulo="Autoridades inactivas",
        estatus="B",
    )


@autoridades.route("/autoridades/<int:autoridad_id>")
def detail(autoridad_id):
    """Detalle de un Autoridad"""
    autoridad = Autoridad.query.get_or_404(autoridad_id)
    return render_template("autoridades/detail.jinja2", autoridad=autoridad)
