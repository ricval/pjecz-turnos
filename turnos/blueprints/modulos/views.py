"""
Modulos, vistas
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.modulos.models import Modulo

modulos = Blueprint("modulos", __name__, template_folder="templates")

MODULO = "MODULOS"


@modulos.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@modulos.route("/modulos")
def list_active():
    """Listado de Modulos activos"""
    return render_template(
        "modulos/list.jinja2",
        modulos=Modulo.query.filter_by(estatus="A").all(),
        titulo="Módulos",
        estatus="A",
    )


@modulos.route("/modulos/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Modulos inactivos"""
    return render_template(
        "modulos/list.jinja2",
        modulos=Modulo.query.filter_by(estatus="B").all(),
        titulo="Módulos inactivos",
        estatus="B",
    )


@modulos.route("/modulos/<int:modulo_id>")
def detail(modulo_id):
    """Detalle de un Modulo"""
    modulo = Modulo.query.get_or_404(modulo_id)
    return render_template("modulos/detail.jinja2", modulo=modulo)
