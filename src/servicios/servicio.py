"""
Módulo: servicio.py
Descripción: Clase abstracta Servicio, hereda de Entidad. Define lo común a
todos los servicios de Software FJ (nombre, precio, disponibilidad) y el
cálculo de costos con impuestos y descuentos. Cada servicio hijo implementa
su propia forma de calcular el costo base y de validar parámetros (polimorfismo).
"""

from abc import abstractmethod
from functools import singledispatchmethod

from src.modelos.entidad import Entidad
from src.excepciones.excepciones import (
    ServicioError, ServicioNoDisponibleError, CalculoInconsistenteError,
    DatoInvalidoError, ParametroFaltanteError,
)

# Cupones de descuento válidos: código -> porcentaje
CUPONES = {"UNAD10": 10, "FJ20": 20, "BIENVENIDA": 15}


def formato_pesos(valor):
    """Convierte un número a formato de pesos colombianos: 150000 -> $150.000"""
    return "$" + f"{valor:,.0f}".replace(",", ".")


class Servicio(Entidad):
    """Clase abstracta base para todos los servicios ofrecidos."""

    def __init__(self, nombre, precio_base):
        super().__init__()  # Id y fecha de creación desde Entidad
        self.nombre = nombre
        self.precio_base = precio_base
        self.__disponible = True  # Todo servicio inicia disponible

    # ---------------- Propiedades con validación ----------------

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre del servicio")
        self.__nombre = str(valor).strip()

    @property
    def precio_base(self):
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if valor is None or valor == "":
            raise ParametroFaltanteError("precio_base")
        try:
            precio = float(valor)  # Puede fallar si viene texto como "abc"
        except (TypeError, ValueError) as e:
            # Encadenamiento: se conserva el error original de Python como causa
            raise ServicioError(f"El precio '{valor}' no es un número válido") from e
        if precio <= 0:
            raise DatoInvalidoError("precio_base", valor, "el precio debe ser mayor que cero")
        self.__precio_base = precio

    @property
    def disponible(self):
        return self.__disponible

    def deshabilitar(self):
        """Marca el servicio como no disponible (ej. sala en mantenimiento)."""
        self.__disponible = False

    def habilitar(self):
        """Vuelve a poner el servicio como disponible."""
        self.__disponible = True

    def verificar_disponibilidad(self):
        """Lanza excepción si el servicio no se puede reservar en este momento."""
        if not self.__disponible:
            raise ServicioNoDisponibleError(self.nombre)
        return True

    # ---------------- Métodos que cada servicio hijo DEBE implementar ----------------

    @abstractmethod
    def _costo_base(self, duracion, **opciones):
        """Costo sin impuestos ni descuentos; cada servicio lo calcula distinto."""

    @abstractmethod
    def validar_parametros(self, duracion, **opciones):
        """Verifica que la duración y opciones sean válidas para este servicio."""

    @abstractmethod
    def unidad(self):
        """Unidad de cobro del servicio: 'hora' o 'día'."""

    def validar(self):
        """Valida los datos generales del servicio (implementa el método de Entidad)."""
        if not self.nombre:
            raise ParametroFaltanteError("nombre del servicio")
        if self.precio_base <= 0:
            raise DatoInvalidoError("precio_base", self.precio_base, "debe ser mayor que cero")
        return True

    # ---------------- Sobrecarga 1: descuento por número o por cupón ----------------
    # singledispatchmethod elige qué versión ejecutar según el TIPO del argumento

    @singledispatchmethod
    def obtener_descuento(self, descuento):
        """Versión general: tipo no soportado."""
        raise DatoInvalidoError("descuento", descuento, "debe ser un porcentaje o un cupón")

    @obtener_descuento.register(int)
    @obtener_descuento.register(float)
    def _(self, descuento):
        """Versión numérica: el descuento es un porcentaje (ej. 10 = 10%)."""
        return float(descuento)

    @obtener_descuento.register(str)
    def _(self, descuento):
        """Versión texto: el descuento es un código de cupón (ej. 'UNAD10')."""
        codigo = descuento.strip().upper()
        if codigo not in CUPONES:
            raise DatoInvalidoError("cupón", descuento, "cupón no existe")
        return float(CUPONES[codigo])

    # ---------------- Sobrecarga 2: parámetros opcionales ----------------

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **opciones):
        """
        Calcula el costo total del servicio. Se puede llamar de varias formas:
          calcular_costo(3)                  -> solo costo base
          calcular_costo(3, impuesto=19)     -> con IVA del 19%
          calcular_costo(3, 19, 10)          -> con IVA y 10% de descuento
          calcular_costo(3, 19, "UNAD10")    -> con IVA y cupón de descuento
        """
        self.validar_parametros(duracion, **opciones)      # Polimórfico: cada hijo valida a su modo
        base = self._costo_base(duracion, **opciones)      # Polimórfico: cada hijo calcula a su modo
        porc_descuento = self.obtener_descuento(descuento) # Sobrecarga por tipo

        # Validación de porcentajes: evita cálculos inconsistentes
        if not 0 <= impuesto <= 100:
            raise CalculoInconsistenteError(f"impuesto de {impuesto}% fuera de rango (0 a 100)")
        if not 0 <= porc_descuento <= 100:
            raise CalculoInconsistenteError(f"descuento de {porc_descuento}% fuera de rango (0 a 100)")

        total = base * (1 - porc_descuento / 100) * (1 + impuesto / 100)
        if total < 0:
            raise CalculoInconsistenteError(f"el total dio negativo ({total})")
        return round(total, 2)

    # ---------------- Método auxiliar para que los hijos validen la duración ----------------

    def _validar_duracion(self, duracion, minimo, maximo):
        """Revisa que la duración exista, sea entera y esté en el rango permitido."""
        if duracion is None or duracion == "":
            raise ParametroFaltanteError("duración")
        if not isinstance(duracion, int) or isinstance(duracion, bool):
            raise DatoInvalidoError("duración", duracion, "debe ser un número entero")
        if not minimo <= duracion <= maximo:
            raise DatoInvalidoError(
                "duración", duracion,
                f"para '{self.nombre}' debe estar entre {minimo} y {maximo} {self.unidad()}s",
            )
