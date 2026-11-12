"""
Módulo: reserva_sala.py
Descripción: Servicio de reserva de salas. Se cobra por hora y tiene una
capacidad máxima de personas. Hereda de Servicio y sobrescribe sus métodos.
"""

from src.servicios.servicio import Servicio, formato_pesos
from src.excepciones.excepciones import DatoInvalidoError


class ReservaSala(Servicio):
    """Alquiler de una sala de reuniones o capacitación, cobrado por hora."""

    HORAS_MIN, HORAS_MAX = 1, 12  # Una sala se reserva entre 1 y 12 horas

    def __init__(self, nombre, precio_hora, capacidad):
        super().__init__(nombre, precio_hora)
        # Validación propia de este servicio: capacidad entera y positiva
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("capacidad", capacidad, "debe ser un entero mayor que cero")
        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    def unidad(self):
        return "hora"

    def validar_parametros(self, duracion, asistentes=1, **opciones):
        """Valida horas y que los asistentes no superen la capacidad de la sala."""
        self._validar_duracion(duracion, self.HORAS_MIN, self.HORAS_MAX)
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise DatoInvalidoError("asistentes", asistentes, "debe ser un entero mayor que cero")
        if asistentes > self.__capacidad:
            raise DatoInvalidoError(
                "asistentes", asistentes, f"la sala solo tiene capacidad para {self.__capacidad}"
            )
        return True

    def _costo_base(self, duracion, **opciones):
        """Precio por hora multiplicado por las horas reservadas."""
        return self.precio_base * duracion

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Sala #{self.id}: {self.nombre} | {formato_pesos(self.precio_base)}/hora | "
                f"Capacidad: {self.__capacidad} personas | {estado}")
