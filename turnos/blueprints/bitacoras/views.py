"""
Bitácoras, vistas
"""
from flask import Blueprint, render_template, url_for
from flask_login import login_required

from lib import datatables

from turnos.blueprints.bitacoras.models import Bitacora
from turnos.blueprints.modulos.models import Modulo
from turnos.blueprints.permisos.models import Permiso
from turnos.blueprints.usuarios.decorators import permission_required

MODULO = "BITACORAS"

bitacoras = Blueprint("bitacoras", __name__, template_folder="templates")


@bitacoras.route("/bitacoras")
@login_required
@permission_required(MODULO, Permiso.VER)
def list_active():
    """Listado de bitácoras"""
    return render_template("bitacoras/list.jinja2")


@bitacoras.route("/bitacoras/datatable_json", methods=["GET", "POST"])
@login_required
@permission_required(MODULO, Permiso.VER)
def datatable_json():
    """DataTable JSON para listado de listado de bitácoras"""
    # Tomar parámetros de Datatables
    draw, start, rows_per_page = datatables.get_parameters()
    # Consultar
    consulta = Bitacora.query
    registros = consulta.order_by(Bitacora.creado.desc()).offset(start).limit(rows_per_page).all()
    total = consulta.count()
    # Elaborar un listado de diccionarios
    data = []
    for bitacora in registros:
        data.append(
            {
                "creado": bitacora.creado.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": {
                    "email": bitacora.usuario.email,
                    "url": url_for("usuarios.detail", usuario_id=bitacora.usuario_id),
                },
                "vinculo": {
                    "descripcion": bitacora.descripcion,
                    "url": bitacora.url,
                },
            }
        )
    # Entregar JSON
    return datatables.output(draw, total, data)
