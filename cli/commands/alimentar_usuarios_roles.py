"""
Alimentar usuarios-roles
"""
from pathlib import Path
import csv
import click

from lib.safe_string import safe_string

from turnos.blueprints.roles.models import Rol
from turnos.blueprints.usuarios.models import Usuario
from turnos.blueprints.usuarios_roles.models import UsuarioRol

USUARIOS_ROLES_CSV = "seed/usuarios_roles.csv"


def alimentar_usuarios_roles():
    """Alimentar usuarios-roles"""
    ruta = Path(USUARIOS_ROLES_CSV)
    if not ruta.exists():
        click.echo(f"AVISO: {ruta.name} no se encontrĂ³.")
        return
    if not ruta.is_file():
        click.echo(f"AVISO: {ruta.name} no es un archivo.")
        return
    usuarios = Usuario.query.filter_by(estatus="A").all()
    if len(usuarios) == 0:
        click.echo("AVISO: Faltan de alimentar los usuarios")
        return
    click.echo("Alimentando usuarios-roles...")
    contador = 0
    with open(ruta, encoding="utf8") as puntero:
        rows = csv.DictReader(puntero)
        for row in rows:
            usuario_id = int(row["usuario_id"])
            usuario = Usuario.query.get(usuario_id)
            if usuario is None:
                click.echo(f"  Falta el usuario_id {str(usuario_id)}")
                return
            for rol_str in row["roles"].split(","):
                rol_str = rol_str.strip().upper()
                rol = Rol.query.filter_by(nombre=rol_str).first()
                if rol is None:
                    click.echo(f"  Falta el rol {rol_str}")
                    continue
                descripcion = f"{usuario.email} en {rol.nombre}"
                UsuarioRol(
                    usuario=usuario,
                    rol=rol,
                    descripcion=descripcion,
                ).save()
                click.echo(f"  {descripcion}")
                contador += 1
    click.echo(f"  {contador} usuarios-roles alimentados.")
