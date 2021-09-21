"""
Permisos, modelos
"""
from turnos.extensions import db
from lib.universal_mixin import UniversalMixin


class Permiso(db.Model, UniversalMixin):
    """Permiso"""

    # Nombre de la tabla
    __tablename__ = "permisos"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Clave foránea
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), index=True, nullable=False)
    rol = db.relationship("Rol", back_populates="permisos")
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulos.id"), index=True, nullable=False)
    modulo = db.relationship("Modulo", back_populates="permisos")

    # Columnas
    nombre = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<Permiso {nombre}>"
