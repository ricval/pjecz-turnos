"""
Usuarios, vistas
"""
import json
import os
import re

import google.auth.transport.requests
import google.oauth2.id_token
from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from lib import datatables
from lib.firebase_auth import firebase_auth
from lib.pwgen import generar_contrasena
from lib.safe_next_url import safe_next_url
from lib.safe_string import CONTRASENA_REGEXP, EMAIL_REGEXP, TOKEN_REGEXP, safe_message

from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import anonymous_required, permission_required
from turnos.extensions import pwd_context

from turnos.blueprints.autoridades.models import Autoridad
from turnos.blueprints.bitacoras.models import Bitacora
from turnos.blueprints.distritos.models import Distrito
from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.entradas_salidas.models import EntradaSalida
from turnos.blueprints.usuarios.forms import AccesoForm, UsuarioFormNew, UsuarioFormEdit
from turnos.blueprints.usuarios.models import Usuario

HTTP_REQUEST = google.auth.transport.requests.Request()

MODULO = "USUARIOS"

usuarios = Blueprint("usuarios", __name__, template_folder="templates")


@usuarios.route("/login", methods=["GET", "POST"])
@anonymous_required()
def login():
    """Acceso al Sistema"""
    form = AccesoForm(siguiente=request.args.get("siguiente"))
    if form.validate_on_submit():
        # Tomar valores del formulario
        identidad = request.form.get("username")
        contrasena = request.form.get("password")
        token = request.form.get("token")
        siguiente_url = request.form.get("siguiente")
        # Si esta definida la variable de entorno FIREBASE_APIKEY
        if os.environ.get("FIREBASE_APIKEY", "") != "":
            # Entonces debe ingresar con Google/Microsoft/GitHub
            if re.fullmatch(TOKEN_REGEXP, token) is not None:
                # Acceso por Firebase Auth
                claims = google.oauth2.id_token.verify_firebase_token(token, HTTP_REQUEST)
                if claims:
                    email = claims.get("email", "Unknown")
                    usuario = Usuario.find_by_identity(email)
                    if usuario and usuario.authenticated(with_password=False):
                        if login_user(usuario, remember=True) and usuario.is_active:
                            EntradaSalida(
                                usuario_id=usuario.id,
                                tipo="INGRESO",
                                direccion_ip=request.remote_addr,
                            ).save()
                            if siguiente_url:
                                return redirect(safe_next_url(siguiente_url))
                            return redirect(url_for("sistemas.start"))
                        else:
                            flash("No est?? activa esa cuenta.", "warning")
                    else:
                        flash("No existe esa cuenta.", "warning")
                else:
                    flash("Fall?? la autentificaci??n.", "warning")
            else:
                flash("Token incorrecto.", "warning")
        elif re.fullmatch(EMAIL_REGEXP, identidad) is not None and re.fullmatch(CONTRASENA_REGEXP, contrasena) is not None:
            # De lo contrario, el ingreso es con username/password
            usuario = Usuario.find_by_identity(identidad)
            if usuario and usuario.authenticated(password=contrasena):
                if login_user(usuario, remember=True) and usuario.is_active:
                    EntradaSalida(
                        usuario_id=usuario.id,
                        tipo="INGRESO",
                        direccion_ip=request.remote_addr,
                    ).save()
                    if siguiente_url:
                        return redirect(safe_next_url(siguiente_url))
                    return redirect(url_for("sistemas.start"))
                else:
                    flash("No est?? activa esa cuenta", "warning")
            else:
                flash("Usuario o contrase??a incorrectos.", "warning")
    return render_template("usuarios/login.jinja2", form=form, firebase_auth=firebase_auth, title="Turnos")


@usuarios.route("/logout")
@login_required
def logout():
    """Salir del Sistema"""
    EntradaSalida(
        usuario_id=current_user.id,
        tipo="SALIO",
        direccion_ip=request.remote_addr,
    ).save()
    logout_user()
    flash("Ha salido de este sistema.", "success")
    return redirect(url_for("usuarios.login"))


@usuarios.route("/perfil")
@login_required
def profile():
    """Mostrar el Perfil"""
    return render_template("usuarios/profile.jinja2")


@usuarios.route("/usuarios")
@login_required
@permission_required(MODULO, Permiso.VER)
def list_active():
    """Listado de Usuarios activos"""
    return render_template(
        "usuarios/list.jinja2",
        filtros=json.dumps({"estatus": "A"}),
        titulo="Usuarios",
        estatus="A",
    )


@usuarios.route("/usuarios/inactivos")
@login_required
@permission_required(MODULO, Permiso.MODIFICAR)
def list_inactive():
    """Listado de Usuarios inactivos"""
    return render_template(
        "usuarios/list.jinja2",
        filtros=json.dumps({"estatus": "B"}),
        titulo="Usuarios inactivos",
        estatus="B",
    )


@usuarios.route("/usuarios/datatable_json", methods=["GET", "POST"])
@login_required
@permission_required(MODULO, Permiso.VER)
def datatable_json():
    """DataTable JSON para listado de usuarios"""
    # Tomar par??metros de Datatables
    draw, start, rows_per_page = datatables.get_parameters()
    # Consultar
    consulta = Usuario.query
    if "estatus" in request.form:
        consulta = consulta.filter_by(estatus=request.form["estatus"])
    else:
        consulta = consulta.filter_by(estatus="A")
    registros = consulta.order_by(Usuario.email).offset(start).limit(rows_per_page).all()
    total = consulta.count()
    # Elaborar datos para DataTable
    data = []
    for usuario in registros:
        data.append(
            {
                "detalle": {
                    "email": usuario.email,
                    "url": url_for("usuarios.detail", usuario_id=usuario.id),
                },
                "nombre": usuario.nombre,
                "puesto": usuario.puesto,
            }
        )
    # Entregar JSON
    return datatables.output(draw, total, data)


@usuarios.route("/usuarios/<int:usuario_id>")
@login_required
@permission_required(MODULO, Permiso.VER)
def detail(usuario_id):
    """Detalle de un Usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template("usuarios/detail.jinja2", usuario=usuario)


@usuarios.route("/usuarios/nuevo", methods=["GET", "POST"])
@login_required
@permission_required(MODULO, Permiso.CREAR)
def new():
    """Nuevo usuario"""
    form = UsuarioFormNew()
    if form.validate_on_submit():
        autoridad = Autoridad.query.get_or_404(form.autoridad.data)
        if form.contrasena.data == "":
            contrasena = pwd_context.hash(generar_contrasena())
        else:
            contrasena = pwd_context.hash(form.contrasena.data)
        usuario = Usuario(
            autoridad=autoridad,
            nombres=form.nombres.data,
            apellido_paterno=form.apellido_paterno.data,
            apellido_materno=form.apellido_materno.data,
            curp=form.curp.data,
            email=form.email.data,
            puesto=form.puesto.data,
            contrasena=contrasena,
        )
        usuario.save()
        bitacora = Bitacora(
            modulo=Modulo.query.filter_by(nombre=MODULO).first(),
            usuario=current_user,
            descripcion=safe_message(f"Nuevo usuario {usuario.email}: {usuario.nombre}"),
            url=url_for("usuarios.detail", usuario_id=usuario.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    distritos = Distrito.query.filter_by(estatus="A").order_by(Distrito.nombre).all()
    autoridades = Autoridad.query.filter_by(estatus="A").order_by(Autoridad.clave).all()
    return render_template("usuarios/new.jinja2", form=form, distritos=distritos, autoridades=autoridades)


@usuarios.route("/usuarios/edicion/<int:usuario_id>", methods=["GET", "POST"])
@login_required
@permission_required(MODULO, Permiso.MODIFICAR)
def edit(usuario_id):
    """Editar Usuario, solo al escribir la contrase??a se cambia"""
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioFormEdit()
    if form.validate_on_submit():
        usuario.nombres = form.nombres.data
        usuario.apellido_paterno = form.apellido_paterno.data
        usuario.apellido_materno = form.apellido_materno.data
        usuario.curp = form.curp.data
        usuario.email = form.email.data
        usuario.puesto = form.puesto.data
        if form.contrasena.data != "":
            usuario.contrasena = pwd_context.hash(form.contrasena.data)
        usuario.save()
        bitacora = Bitacora(
            modulo=Modulo.query.filter_by(nombre=MODULO).first(),
            usuario=current_user,
            descripcion=safe_message(f"Editado usuario {usuario.email}: {usuario.nombre}"),
            url=url_for("usuarios.detail", usuario_id=usuario.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
        return redirect(bitacora.url)
    form.nombres.data = usuario.nombres
    form.apellido_paterno.data = usuario.apellido_paterno
    form.apellido_materno.data = usuario.apellido_materno
    form.curp.data = usuario.curp
    form.email.data = usuario.email
    form.puesto.data = usuario.puesto
    return render_template("usuarios/edit.jinja2", form=form, usuario=usuario)


@usuarios.route("/usuarios/eliminar/<int:usuario_id>")
@login_required
@permission_required(MODULO, Permiso.MODIFICAR)
def delete(usuario_id):
    """Eliminar Usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.estatus == "A":
        usuario.delete()
        bitacora = Bitacora(
            modulo=Modulo.query.filter_by(nombre=MODULO).first(),
            usuario=current_user,
            descripcion=safe_message(f"Eliminado usuario {usuario.email}: {usuario.nombre}"),
            url=url_for("usuarios.detail", usuario_id=usuario.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
    return redirect(url_for("usuarios.detail", usuario_id=usuario_id))


@usuarios.route("/usuarios/recuperar/<int:usuario_id>")
@login_required
@permission_required(MODULO, Permiso.MODIFICAR)
def recover(usuario_id):
    """Recuperar Usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.estatus == "B":
        usuario.recover()
        bitacora = Bitacora(
            modulo=Modulo.query.filter_by(nombre=MODULO).first(),
            usuario=current_user,
            descripcion=safe_message(f"Recuperado usuario {usuario.email}: {usuario.nombre}"),
            url=url_for("usuarios.detail", usuario_id=usuario.id),
        )
        bitacora.save()
        flash(bitacora.descripcion, "success")
    return redirect(url_for("usuarios.detail", usuario_id=usuario_id))
