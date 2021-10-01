"""
Usuarios Roles, vistas
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.usuarios_roles.models import UsuarioRol

usuarios_roles = Blueprint("usuarios_roles", __name__, template_folder="templates")

MODELO = "USUARIOS_ROLES"


@usuarios_roles.before_request
@login_required
@permission_required(MODELO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@usuarios_roles.route("/usuarios_roles")
def list_active():
    """Listado de Usuarios Roles activos"""
    usuarios_roles_activos = UsuarioRol.query.filter(UsuarioRol.estatus == "A").all()
    return render_template(
        "usuarios_roles/list.jinja2",
        usuarios_roles=usuarios_roles_activos,
        titulo="Usuarios-Roles",
        estatus="A",
    )


@usuarios_roles.route("/usuarios_roles/inactivos")
@permission_required(MODELO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Usuarios Roles inactivos"""
    usuarios_roles_inactivos = UsuarioRol.query.filter(UsuarioRol.estatus == "B").all()
    return render_template(
        "usuarios_roles/list.jinja2",
        usuarios_roles=usuarios_roles_inactivos,
        titulo="Usuarios-Roles inactivos",
        estatus="B",
    )


@usuarios_roles.route("/usuarios_roles/<int:usuario_rol_id>")
def detail(usuario_rol_id):
    """Detalle de un Usuario Rol"""
    usuario_rol = UsuarioRol.query.get_or_404(usuario_rol_id)
    return render_template("usuarios_roles/detail.jinja2", usuario_rol=usuario_rol)
