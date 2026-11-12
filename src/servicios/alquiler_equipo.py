"""
Módulo: alquiler_equipo.py
Descripción: Servicio de alquiler de equipos (portátiles, proyectores, etc.).
Se cobra por día y por cantidad de unidades, más un seguro del 5%.
Hereda de Servicio y sobrescribe sus métodos.
"""

from src.servicios.servicio import Servicio, formato_pesos
from src.excepciones.excepciones import DatoInvalidoError


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos, cobrado por día y por unidad."""

    DIAS_MIN, DIAS_MAX = 1, 30   # Se alquila entre 1 y 30 días
    PORC_SEGURO = 5              # Seguro obligatorio sobre el costo base (%)

    def __init__(self, nombre, precio_dia, unidades_disponibles):
        super().__init__(nombre, precio_dia)
        if not isinstance(unidades_disponibles, int) or unidades_disponibles <= 0:
            raise DatoInvalidoError("unidades_disponibles", unidades_disponibles,
                                    "debe ser un entero mayor que cero")
        self.__unidades = unidades_disponibles

    @property
    def unidades_disponibles(self):
        return self.__unidades

    def unidad(self):
        return "día"

    def validar_parametros(self, duracion, cantidad=1, **opciones):
        """Valida días y que la cantidad pedida no supere las unidades en inventario."""
        self._validar_duracion(duracion, self.DIAS_MIN, self.DIAS_MAX)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("cantidad", cantidad, "debe ser un entero mayor que cero")
        if cantidad > self.__unidades:
            raise DatoInvalidoError(
                "cantidad", cantidad, f"solo hay {self.__unidades} unidades disponibles"
            )
        return True

    def _costo_base(self, duracion, cantidad=1, **opciones):
        """Precio por día × días × unidades, más el seguro obligatorio."""
        subtotal = self.precio_base * duracion * cantidad
        return subtotal * (1 + self.PORC_SEGURO / 100)

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Equipo #{self.id}: {self.nombre} | {formato_pesos(self.precio_base)}/día | "
                f"Unidades: {self.__unidades} | Seguro {self.PORC_SEGURO}% | {estado}")
