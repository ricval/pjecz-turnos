"""
Roles, modelos
"""
from turnos.extensions import db
from lib.universal_mixin import UniversalMixin


class Permiso:
    """Permiso tiene como constantes enteros de potencia dos"""

    # CUENTAS
    VER_CUENTAS = 0b1
    MODIFICAR_CUENTAS = 0b10
    CREAR_CUENTAS = MODIFICAR_CUENTAS

    # TURNOS
    VER_TURNOS = 0b100
    MODIFICAR_TURNOS = 0b1000
    CREAR_TURNOS = MODIFICAR_TURNOS

    def __repr__(self):
        """Representación"""
        return "<Permiso>"


class Rol(db.Model, UniversalMixin):
    """Rol"""

    # Nombre de la tabla
    __tablename__ = "roles"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Columnas
    nombre = db.Column(db.String(256), unique=True, nullable=False)
    permiso = db.Column(db.Integer, nullable=False)
    por_defecto = db.Column(db.Boolean, default=False, index=True)

    # Hijos
    usuarios = db.relationship("Usuario", back_populates="rol")

    def add_permission(self, perm):
        """Agregar permiso"""
        if not self.has_permission(perm):
            self.permiso += perm

    def remove_permission(self, perm):
        """Retirar permiso"""
        if self.has_permission(perm):
            self.permiso -= perm

    def reset_permissions(self):
        """Poner permisos a cero"""
        self.permiso = 0

    def has_permission(self, perm):
        """¿Tiene el permiso dado?"""
        return self.permiso & perm == perm

    @staticmethod
    def insert_roles():
        """Insertar roles iniciales"""
        roles = {
            "ADMINISTRADOR": [
                Permiso.VER_CUENTAS,
                Permiso.MODIFICAR_CUENTAS,
                Permiso.CREAR_CUENTAS,
                Permiso.VER_TURNOS,
            ],
            "SOPORTE TECNICO": [
                Permiso.VER_CUENTAS,
                Permiso.VER_TURNOS,
                Permiso.MODIFICAR_TURNOS,
                Permiso.CREAR_TURNOS,
            ],
            "USUARIO": [
                Permiso.VER_CUENTAS,
                Permiso.VER_TURNOS,
                Permiso.MODIFICAR_TURNOS,
                Permiso.CREAR_TURNOS,
            ],
            "OBSERVADOR": [
                Permiso.VER_CUENTAS,
                Permiso.VER_TURNOS,
            ],
        }
        rol_por_defecto = "OBSERVADOR"
        for item in roles:
            rol = Rol.query.filter_by(nombre=item).first()
            if rol is None:
                rol = Rol(nombre=item)
            rol.reset_permissions()
            for perm in roles[item]:
                rol.add_permission(perm)
            rol.por_defecto = rol.nombre == rol_por_defecto
            db.session.add(rol)
        db.session.commit()
        return len(roles)

    def can_view(self, module):
        """¿Tiene permiso para ver?"""
        if module in ("bitacoras", "entradas_salidas", "modulos", "roles", "usuarios"):
            return self.has_permission(Permiso.VER_CUENTAS)
        if module in ("FUTURO1", "FUTURO2", "FUTURO3", "FUTURO4"):
            return self.has_permission(Permiso.VER_TURNOS)
        return False

    def can_insert(self, module):
        """¿Tiene permiso para agregar?"""
        if module in ("bitacoras", "entradas_salidas", "modulos", "roles", "usuarios"):
            return self.has_permission(Permiso.MODIFICAR_CUENTAS)
        if module in ("FUTURO1", "FUTURO2", "FUTURO3", "FUTURO4"):
            return self.has_permission(Permiso.MODIFICAR_TURNOS)
        return False

    def can_edit(self, module):
        """¿Tiene permiso para editar?"""
        if module in ("bitacoras", "entradas_salidas", "modulos", "roles", "usuarios"):
            return self.has_permission(Permiso.CREAR_CUENTAS)
        if module in ("distritos", "autoridades", "materias", "materias_tipos_juicios"):
            return self.has_permission(Permiso.CREAR_TURNOS)
        return False

    def can_admin(self, module):
        """¿Tiene permiso para administrar?"""
        return False

    def __repr__(self):
        """Representación"""
        return f"<Rol {self.nombre}>"