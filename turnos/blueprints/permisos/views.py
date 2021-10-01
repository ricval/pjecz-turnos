"""
Permisos, vistas
"""
from flask import Blueprint, render_template
from flask_login import login_required

from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required

permisos = Blueprint("permisos", __name__, template_folder="templates")

MODULO = "PERMISOS"


@permisos.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@permisos.route("/permisos")
def list_active():
    """Listado de Permisos activos"""
    return render_template(
        "permisos/list.jinja2",
        permisos=Permiso.query.filter_by(estatus="A").all(),
        titulo="Permisos",
        estatus="A",
    )


@permisos.route("/permisos/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Permisos inactivos"""
    return render_template(
        "permisos/list.jinja2",
        permisos=Permiso.query.filter_by(estatus="B").all(),
        titulo="Permisos inactivos",
        estatus="B",
    )


@permisos.route("/permisos/<int:permiso_id>")
def detail(permiso_id):
    """Detalle de un Permiso"""
    permiso = Permiso.query.get_or_404(permiso_id)
    return render_template("permisos/detail.jinja2", permiso=permiso)
