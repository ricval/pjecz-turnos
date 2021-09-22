"""
Permisos, vistas
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from turnos.blueprints.roles.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.permisos.models import Permiso

permisos = Blueprint("permisos", __name__, template_folder="templates")


@permisos.before_request
@login_required
@permission_required(Permiso.VER_CUENTAS)
def before_request():
    """Permiso por defecto"""


@permisos.route("/permisos")
def list_active():
    """Listado de Permisos activos"""
    permisos_activos = Permiso.query.filter_by(estatus="A").order_by(Permiso.nombre).all()
    return render_template("permisos/list.jinja2", permisos=permisos_activos, estatus="A")


@permisos.route("/permisos/inactivos")
@permission_required(Permiso.MODIFICAR_)
def list_inactive():
    """Listado de Permisos inactivos"""
    permisos_inactivos = Permiso.query.filter_by(estatus="B").order_by(Permiso.nombre).all()
    return render_template("permisos/list.jinja2", permisos=permisos_inactivos, estatus="B")


@permisos.route("/permisos/<int:permiso_id>")
def detail(permiso_id):
    """Detalle de un Permiso"""
    permiso = Permiso.query.get_or_404(permiso_id)
    return render_template("permisos/detail.jinja2", permiso=permiso)
