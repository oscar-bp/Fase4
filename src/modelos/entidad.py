"""
Módulo: entidad.py
Descripción: Clase abstracta Entidad, base de todos los objetos del sistema
(Cliente, Servicio, Reserva). Define lo que todos comparten: un id único,
la fecha de creación y los métodos obligatorios describir() y validar().
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta: no se puede instanciar directamente, solo heredar."""

    # Contador compartido por todas las entidades para generar ids únicos
    _contador = 0

    def __init__(self):
        # Cada vez que se crea una entidad, el contador aumenta en 1
        Entidad._contador += 1
        self.__id = Entidad._contador                 # Id privado y único
        self.__fecha_creacion = datetime.now()        # Momento en que se creó

    # ---------------- Propiedades de solo lectura ----------------

    @property
    def id(self):
        """Id único de la entidad (no se puede modificar)."""
        return self.__id

    @property
    def fecha_creacion(self):
        """Fecha y hora de creación en formato legible."""
        return self.__fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")

    # ---------------- Métodos abstractos ----------------
    # Las clases hijas ESTÁN OBLIGADAS a implementarlos (polimorfismo)

    @abstractmethod
    def describir(self):
        """Devuelve un texto que describe la entidad."""

    @abstractmethod
    def validar(self):
        """Verifica que la entidad tenga datos correctos; lanza excepción si no."""

    def __str__(self):
        # Al imprimir cualquier entidad se usa su propia descripción
        return self.describir()
