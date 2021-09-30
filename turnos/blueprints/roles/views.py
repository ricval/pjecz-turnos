"""
Roles, vistas
"""
from flask import Blueprint, render_template
from flask_login import login_required

from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.roles.models import Rol
from turnos.blueprints.usuarios.models import Usuario

roles = Blueprint('roles', __name__, template_folder='templates')

MODULO = "ROLES"


@roles.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@roles.route('/roles')
def list_active():
    """ Listado de roles """
    roles_activos = Rol.query.filter(Rol.estatus == 'A').order_by(Rol.nombre).all()
    return render_template('roles/list.jinja2', roles=roles_activos)


@roles.route('/roles/inactivos')
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """ Listado de Roles inactivos """
    roles_inactivos = Rol.query.filter(Rol.estatus == 'B').order_by(Rol.nombre).all()
    return render_template('roles/list.jinja2', roles=roles_inactivos, estatus='B')


@roles.route('/roles/<int:rol_id>')
def detail(rol_id):
    """ Detalle de un rol """
    rol = Rol.query.get_or_404(rol_id)
    usuarios = Usuario.query.filter(Usuario.rol == rol).all()
    return render_template('roles/detail.jinja2', rol=rol, usuarios=usuarios)
