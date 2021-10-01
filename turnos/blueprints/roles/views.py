"""
Roles, vistas
"""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from lib.safe_string import safe_message

from turnos.blueprints.bitacoras.models import Bitacora
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required
from turnos.blueprints.roles.models import Rol
from turnos.blueprints.roles.forms import RolForm

roles = Blueprint("roles", __name__, template_folder="templates")

MODULO = "ROLES"


@roles.before_request
@login_required
@permission_required(MODULO, Permiso.VER)
def before_request():
    """Permiso por defecto"""


@roles.route("/roles")
def list_active():
    """Listado de roles"""
    return render_template(
        "roles/list.jinja2",
        roles=Rol.query.filter(Rol.estatus == "A").all(),
        titulo="Roles",
        estatus="A",
    )


@roles.route("/roles/inactivos")
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Roles inactivos"""
    return render_template(
        "roles/list.jinja2",
        roles=Rol.query.filter(Rol.estatus == "B").all(),
        titulo="Roles inactivos",
        estatus="B",
    )


@roles.route("/roles/<int:rol_id>")
def detail(rol_id):
    """Detalle de un rol"""
    rol = Rol.query.get_or_404(rol_id)
    return render_template("roles/detail.jinja2", rol=rol)


@roles.route("/roles/nuevo", methods=["GET", "POST"])
@permission_required(MODULO, Permiso.CREAR)
def new():
    """Nuevo Rol"""
    form = RolForm()
    if form.validate_on_submit():
        rol = Rol(nombre=form.nombre.data)
        rol.save()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Nuevo rol {rol.nombre}"),
            url=url_for("roles.detail", rol_id=rol.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    return render_template("roles/new.jinja2", form=form)


@roles.route("/roles/edicion/<int:rol_id>", methods=["GET", "POST"])
@permission_required(MODULO, Permiso.MODIFICAR)
def edit(rol_id):
    """Editar Rol"""
    rol = Rol.query.get_or_404(rol_id)
    form = RolForm()
    if form.validate_on_submit():
        rol.nombre = form.nombre.data
        rol.save()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Editado rol {rol.nombre}"),
            url=url_for("roles.detail", rol_id=rol.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    form.nombre.data = rol.nombre
    return render_template("roles/edit.jinja2", form=form, rol=rol)


@roles.route("/rol/eliminar/<int:rol_id>")
@permission_required(MODULO, Permiso.MODIFICAR)
def delete(rol_id):
    """Eliminar Rol"""
    rol = Rol.query.get_or_404(rol_id)
    if rol.estatus == "A":
        rol.delete()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Eliminado rol {rol.nombre}"),
            url=url_for("roles.detail", rol_id=rol.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    return redirect(url_for("rol.detail", rol_id=rol.id))


@roles.route("/roles/recuperar/<int:rol_id>")
@permission_required(MODULO, Permiso.MODIFICAR)
def recover(rol_id):
    """Recuperar Rol"""
    rol = Rol.query.get_or_404(rol_id)
    if rol.estatus == "B":
        rol.recover()
        bitacora = Bitacora(
            modulo=MODULO,
            usuario=current_user,
            descripcion=safe_message(f"Recuperado rol {rol.nombre}"),
            url=url_for("roles.detail", rol_id=rol.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    return redirect(url_for("roles.detail", rol_id=rol.id))
