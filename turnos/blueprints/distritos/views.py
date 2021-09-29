"""
Distritos, vistas
"""
from flask import Blueprint, render_template
from flask_login import login_required

from turnos.blueprints.roles.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.distritos.models import Distrito

distritos = Blueprint('distritos', __name__, template_folder='templates')


@distritos.before_request
@login_required
@permission_required(Permiso.VER_CUENTAS)
def before_request():
    """ Permiso por defecto """


@distritos.route('/distritos')
def list_active():
    """ Listado de Distritos activos """
    distritos_activos = Distrito.query.filter(Distrito.estatus == 'A').order_by(Distrito.nombre).all()
    return render_template('distritos/list.jinja2', distritos=distritos_activos, estatus='A')


@distritos.route('/distritos/inactivos')
@permission_required(Permiso.MODIFICAR_CUENTAS)
def list_inactive():
    """ Listado de Distritos inactivos """
    distritos_inactivos = Distrito.query.filter(Distrito.estatus == 'B').order_by(Distrito.nombre).all()
    return render_template('distritos/list.jinja2', distritos=distritos_inactivos, estatus='B')


@distritos.route('/distrito/<int:distrito_id>')
def detail(distrito_id):
    """ Detalle de un Distrito """
    distrito = Distrito.query.get_or_404(distrito_id)
    return render_template('distrito/detail.jinja2', distrito=distrito)
