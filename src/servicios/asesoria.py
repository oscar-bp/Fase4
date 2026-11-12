"""
Módulo: asesoria.py
Descripción: Servicio de asesorías especializadas. Se cobra por hora y el
precio cambia según el nivel (básico o avanzado). Hereda de Servicio
y sobrescribe sus métodos.
"""

from src.servicios.servicio import Servicio, formato_pesos
from src.excepciones.excepciones import DatoInvalidoError, ParametroFaltanteError


class Asesoria(Servicio):
    """Asesoría especializada (ej. desarrollo web, redes), cobrada por hora."""

    HORAS_MIN, HORAS_MAX = 1, 8
    # Multiplicador del precio según el nivel de la asesoría
    NIVELES = {"basico": 1.0, "avanzado": 1.5}

    def __init__(self, nombre, precio_hora, especialidad):
        super().__init__(nombre, precio_hora)
        if especialidad is None or str(especialidad).strip() == "":
            raise ParametroFaltanteError("especialidad")
        self.__especialidad = str(especialidad).strip()

    @property
    def especialidad(self):
        return self.__especialidad

    def unidad(self):
        return "hora"

    def validar_parametros(self, duracion, nivel="basico", **opciones):
        """Valida horas y que el nivel sea uno de los permitidos."""
        self._validar_duracion(duracion, self.HORAS_MIN, self.HORAS_MAX)
        if str(nivel).lower() not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel,
                                    f"debe ser uno de: {', '.join(self.NIVELES)}")
        return True

    def _costo_base(self, duracion, nivel="basico", **opciones):
        """Precio por hora × horas × multiplicador del nivel."""
        return self.precio_base * duracion * self.NIVELES[str(nivel).lower()]

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Asesoría #{self.id}: {self.nombre} ({self.__especialidad}) | "
                f"{formato_pesos(self.precio_base)}/hora | Avanzado x1.5 | {estado}")
