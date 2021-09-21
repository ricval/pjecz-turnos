"""
Usuarios Roles, vistas
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from turnos.blueprints.roles.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.usuarios_roles.models import UsuarioRol

usuarios_roles = Blueprint("usuarios_roles", __name__, template_folder="templates")


@usuarios_roles.before_request
@login_required
@permission_required(Permiso.VER_CUENTAS)
def before_request():
    """Permiso por defecto"""
