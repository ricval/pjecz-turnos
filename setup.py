"""
Comandos Click para instalar con pip install --editable .
"""
from setuptools import setup


setup(
    name="turnos",
    version="0.1",
    entry_points="""
        [console_scripts]
        turnos=cli.cli:cli
    """,
)
