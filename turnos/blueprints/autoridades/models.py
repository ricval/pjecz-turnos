"""
Autoridades, modelos
"""
from turnos.extensions import db
from lib.universal_mixin import UniversalMixin


class Autoridad(db.Model, UniversalMixin):
    """Autoridad"""

    # Nombre de la tabla
    __tablename__ = "autoridades"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Clave foránea
    distrito_id = db.Column(db.Integer, db.ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = db.relationship("Distrito", back_populates="autoridades")

    # Columnas
    clave = db.Column(db.String(16), nullable=False, unique=True)
    descripcion = db.Column(db.String(256), nullable=False)
    descripcion_corta = db.Column(db.String(64), nullable=False, default="", server_default="")
    es_jurisdiccional = db.Column(db.Boolean, nullable=False, default=False)

    # Hijos
    usuarios = db.relationship("Usuario", back_populates="autoridad")

    def __repr__(self):
        """Representación"""
        return "<Autoridad>"
