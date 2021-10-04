"""
Distritos, vistas
"""
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required

from turnos.blueprints.distritos.models import Distrito
from turnos.blueprints.distritos.forms import DistritoForm
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required

MODULO = "DISTRITOS"

distritos = Blueprint("distritos", __name__, template_folder="templates")


@distritos.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@distritos.route("/distritos")
def list_active():
    """Listado de Distritos activos"""
    return render_template(
        "distritos/list.jinja2",
        distritos=Distrito.query.filter(Distrito.estatus == "A").all(),
        titulo="Distritos",
        estatus="A",
    )


@distritos.route("/distritos/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Distritos inactivos"""
    return render_template(
        "distritos/list.jinja2",
        distritos=Distrito.query.filter(Distrito.estatus == "B").all(),
        titulo="Distritos inactivos",
        estatus="B",
    )


@distritos.route("/distrito/<int:distrito_id>")
def detail(distrito_id):
    """Detalle de un Distrito"""
    distrito = Distrito.query.get_or_404(distrito_id)
    return render_template("distrito/detail.jinja2", distrito=distrito)


@distritos.route("/distritos/nuevo", methods=["GET", "POST"])
@permission_required(MODULO, Permiso.CREAR)
def new():
    """Nuevo Distrito"""
    form = DistritoForm()
    if form.validate_on_submit():
        distrito = Distrito(nombre=form.nombre.data)
        distrito.save()
        flash(f"Distrito {distrito.nombre} guardado.", "success")
        return redirect(url_for("distritos.detail", distrito_id=distrito.id))
    return render_template("distritos/new.jinja2", form=form)
