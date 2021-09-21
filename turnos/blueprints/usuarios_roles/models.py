"""
Usuarios Roles, modelos
"""
from turnos.extensions import db
from lib.universal_mixin import UniversalMixin


class UsuarioRol(db.Model, UniversalMixin):
    """UsuarioRol"""

    # Nombre de la tabla
    __tablename__ = "usuarios_roles"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Clave foránea
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = db.relationship("Usuario", back_populates="usuarios_roles")

    # Columnas
    descripcion = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        """Representación"""
        return "<UsuarioRol>"
