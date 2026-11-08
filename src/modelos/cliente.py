"""
Módulo: cliente.py
Descripción: Clase Cliente, hereda de Entidad. Guarda los datos personales
en atributos privados (encapsulación) y los valida con reglas estrictas
cada vez que se asignan, usando las excepciones personalizadas del Bloque 1.
"""

import re

from src.modelos.entidad import Entidad
from src.excepciones.excepciones import DatoInvalidoError, ParametroFaltanteError

# Expresiones regulares para validar el formato de cada dato
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{3,60}$")        # Solo letras y espacios
PATRON_DOCUMENTO = re.compile(r"^\d{6,10}$")                          # 6 a 10 dígitos
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")           # usuario@dominio.ext
PATRON_TELEFONO = re.compile(r"^3\d{9}$")                             # Celular Colombia: 10 dígitos, inicia en 3


class Cliente(Entidad):
    """Representa un cliente de Software FJ con sus datos personales protegidos."""

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()  # Asigna id y fecha de creación desde Entidad
        # Se usan los setters para que cada dato pase por su validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------------- Método auxiliar de validación ----------------

    @staticmethod
    def _verificar(campo, valor, patron, detalle):
        """Valida que el valor exista y cumpla el patrón; si no, lanza excepción."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(campo)
        valor = str(valor).strip()
        if not patron.match(valor):
            raise DatoInvalidoError(campo, valor, detalle)
        return valor

    # ---------------- Propiedades con validación (encapsulación) ----------------

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._verificar("nombre", valor, PATRON_NOMBRE,
                                "solo letras y espacios, entre 3 y 60 caracteres")
        self.__nombre = valor.title()  # Guarda con mayúscula inicial

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        self.__documento = self._verificar("documento", valor, PATRON_DOCUMENTO,
                                           "debe tener solo números, entre 6 y 10 dígitos")

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._verificar("correo", valor, PATRON_CORREO,
                                "formato de correo incorrecto (ej. usuario@dominio.com)")
        self.__correo = valor.lower()

    @property
    def telefono(self):
        # Por privacidad solo se muestran los últimos 4 dígitos
        return "******" + self.__telefono[-4:]

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = self._verificar("telefono", valor, PATRON_TELEFONO,
                                          "celular de 10 dígitos que inicie en 3")

    # ---------------- Métodos obligatorios de Entidad ----------------

    def validar(self):
        """Revalida todos los datos del cliente; devuelve True si todo está bien."""
        self._verificar("nombre", self.__nombre, PATRON_NOMBRE, "nombre inválido")
        self._verificar("documento", self.__documento, PATRON_DOCUMENTO, "documento inválido")
        self._verificar("correo", self.__correo, PATRON_CORREO, "correo inválido")
        self._verificar("telefono", self.__telefono, PATRON_TELEFONO, "teléfono inválido")
        return True

    def describir(self):
        """Descripción del cliente (polimorfismo: cada entidad se describe distinto)."""
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"Correo: {self.correo} | Tel: {self.telefono}")
