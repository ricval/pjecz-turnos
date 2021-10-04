"""
Alimentar modulos
"""
from pathlib import Path
import csv
import click

from lib.safe_string import safe_string

from turnos.blueprints.modulos.models import Modulo

MODULOS_CSV = "seed/modulos.csv"


def alimentar_modulos():
    """Alimentar modulos"""
    ruta = Path(MODULOS_CSV)
    if not ruta.exists():
        click.echo(f"AVISO: {ruta.name} no se encontró.")
        return
    if not ruta.is_file():
        click.echo(f"AVISO: {ruta.name} no es un archivo.")
        return
    click.echo("Alimentando módulos...")
    contador = 0
    with open(ruta, encoding="utf8") as puntero:
        rows = csv.DictReader(puntero)
        for row in rows:
            nombre = safe_string(row["nombre"])
            Modulo(
                nombre=nombre,
                estatus=row["estatus"],
            ).save()
            click.echo(f"  {nombre}")
            contador += 1
    click.echo(f"  {contador} módulos alimentados.")
