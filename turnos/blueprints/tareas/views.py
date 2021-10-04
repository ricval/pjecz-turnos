"""
Tareas, vistas
"""
from flask import Blueprint, render_template
from flask_login import login_required

from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.tareas.models import Tarea

MODULO = "TAREAS"

tareas = Blueprint("tareas", __name__, template_folder="templates")


@tareas.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@tareas.route("/tareas")
def list_active():
    """Listado de Tareas activas"""
    return render_template(
        "tareas/list.jinja2",
        tareas=Tarea.query.filter_by(estatus="A").all(),
        titulo="Tareas",
        estatus="A",
    )


@tareas.route("/tareas/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Tareas inactivas"""
    return render_template(
        "tareas/list.jinja2",
        tareas=Tarea.query.filter_by(estatus="B").all(),
        titulo="Tareas inactivas",
        estatus="B",
    )
