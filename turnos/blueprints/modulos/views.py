"""
Modulos, vistas
"""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from lib.safe_string import safe_message, safe_string

from turnos.blueprints.bitacoras.models import Bitacora
from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.modulos.forms import ModuloForm
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required

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


@modulos.route("/modulos/nuevo", methods=["GET", "POST"])
@permission_required(MODULO, Permiso.CREAR)
def new():
    """Nuevo Modulo"""
    form = ModuloForm()
    if form.validate_on_submit():
        modulo = Modulo(nombre=safe_string(form.nombre.data))
        modulo.save()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Nuevo módulo {modulo.nombre}"),
            url=url_for("modulos.detail", modulo_id=modulo.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    return render_template("modulos/new.jinja2", form=form)


@modulos.route("/modulos/edicion/<int:modulo_id>", methods=["GET", "POST"])
@permission_required(MODULO, Permiso.MODIFICAR)
def edit(modulo_id):
    """Editar Modulo"""
    modulo = Modulo.query.get_or_404(modulo_id)
    form = ModuloForm()
    if form.validate_on_submit():
        modulo.nombre = safe_string(form.nombre.data)
        modulo.save()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Editado módulo {modulo.nombre}"),
            url=url_for("modulos.detail", modulo_id=modulo.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    form.nombre.data = modulo.nombre
    return render_template("modulos/edit.jinja2", form=form, modulo=modulo)


@modulos.route('/modulos/eliminar/<int:modulo_id>')
@permission_required(MODULO, Permiso.MODIFICAR)
def delete(modulo_id):
    """ Eliminar Modulo """
    modulo = Modulo.query.get_or_404(modulo_id)
    if modulo.estatus == 'A':
        modulo.delete()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f'Eliminado módulo {modulo.nombre}'),
            url=url_for('modulos.detail', modulo_id=modulo.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, 'success')
        return redirect(bitacora.url)
    return redirect(url_for('modulos.detail', modulo_id=modulo.id))


@modulos.route('/modulos/recuperar/<int:modulo_id>')
@permission_required(MODULO, Permiso.MODIFICAR)
def recover(modulo_id):
    """ Recuperar Modulo """
    modulo = Modulo.query.get_or_404(modulo_id)
    if modulo.estatus == 'B':
        modulo.recover()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f'Recuperado módulo {modulo.nombre}'),
            url=url_for('modulos.detail', modulo_id=modulo.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, 'success')
        return redirect(bitacora.url)
    return redirect(url_for('modulos.detail', modulo_id=modulo.id))
