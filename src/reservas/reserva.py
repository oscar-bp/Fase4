"""
Módulo: reserva.py
Descripción: Clase Reserva, hereda de Entidad. Une un Cliente con un Servicio,
una duración y sus opciones. Controla el ciclo de vida de la reserva mediante
estados (PENDIENTE -> CONFIRMADA -> PROCESADA, o CANCELADA) y maneja los
errores con try/except/else/finally y encadenamiento de excepciones.
"""

from src.modelos.entidad import Entidad
from src.modelos.cliente import Cliente
from src.servicios.servicio import Servicio, formato_pesos
from src.excepciones.excepciones import (
    SoftwareFJError, ReservaError, OperacionNoPermitidaError,
    DatoInvalidoError, ParametroFaltanteError,
)
from src.utils.logger import logger


class Reserva(Entidad):
    """Reserva de un servicio hecha por un cliente."""

    # Estados posibles de una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion, impuesto=19, descuento=0, **opciones):
        # Se valida ANTES de crear la entidad para no gastar un id en una reserva inválida
        self._validar_objetos(cliente, servicio)
        super().__init__()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__impuesto = impuesto
        self.__descuento = descuento
        self.__opciones = opciones        # Ej. asistentes=8, cantidad=2, nivel="avanzado"
        self.__estado = Reserva.PENDIENTE  # Toda reserva inicia pendiente
        self.__costo = None                # Se calcula al confirmar
        self.__motivo_cancelacion = None

    # ---------------- Validación de los objetos recibidos ----------------

    @staticmethod
    def _validar_objetos(cliente, servicio):
        """Verifica que lleguen un Cliente y un Servicio reales."""
        if cliente is None:
            raise ParametroFaltanteError("cliente")
        if servicio is None:
            raise ParametroFaltanteError("servicio")
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("cliente", cliente, "debe ser un objeto Cliente registrado")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("servicio", servicio, "debe ser un objeto Servicio registrado")

    # ---------------- Propiedades de solo lectura (encapsulación) ----------------

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # ---------------- Método auxiliar de estados ----------------

    def _exigir_estado(self, operacion, *permitidos):
        """Lanza OperacionNoPermitidaError si el estado actual no está entre los permitidos."""
        if self.__estado not in permitidos:
            raise OperacionNoPermitidaError(operacion, self.__estado)

    # ---------------- Operaciones de la reserva ----------------

    def confirmar(self):
        """
        Confirma la reserva: revisa disponibilidad y calcula el costo.
        try/except/else/finally:
          - try:     intenta verificar y calcular
          - except:  si falla, encadena el error original dentro de un ReservaError
          - else:    solo si todo salió bien, cambia el estado a CONFIRMADA
          - finally: siempre registra que hubo un intento de confirmación
        """
        self._exigir_estado("confirmar", Reserva.PENDIENTE)
        try:
            self.__servicio.verificar_disponibilidad()
            costo = self.__servicio.calcular_costo(
                self.__duracion, self.__impuesto, self.__descuento, **self.__opciones
            )
        except SoftwareFJError as e:
            # Encadenamiento: el error del servicio queda guardado como causa
            raise ReservaError(f"No se pudo confirmar la reserva #{self.id}") from e
        else:
            self.__costo = costo
            self.__estado = Reserva.CONFIRMADA
            logger.info(f"Reserva #{self.id} confirmada: {self.__cliente.nombre} -> "
                        f"{self.__servicio.nombre} por {formato_pesos(costo)}")
        finally:
            logger.info(f"Intento de confirmar reserva #{self.id} finalizado "
                        f"(estado: {self.__estado})")
        return self.__costo

    def cancelar(self, motivo="Sin motivo"):
        """Cancela la reserva. No se puede cancelar una ya cancelada o ya procesada."""
        self._exigir_estado("cancelar", Reserva.PENDIENTE, Reserva.CONFIRMADA)
        self.__estado = Reserva.CANCELADA
        self.__motivo_cancelacion = motivo
        logger.info(f"Reserva #{self.id} cancelada. Motivo: {motivo}")
        return True

    def procesar(self):
        """
        Procesa (ejecuta y cobra) una reserva confirmada y devuelve su factura.
        Vuelve a verificar la disponibilidad por si el servicio cambió después de confirmar.
        """
        self._exigir_estado("procesar", Reserva.CONFIRMADA)
        try:
            self.__servicio.verificar_disponibilidad()
        except SoftwareFJError as e:
            raise ReservaError(f"No se pudo procesar la reserva #{self.id}") from e
        else:
            self.__estado = Reserva.PROCESADA
            logger.info(f"Reserva #{self.id} procesada. Total cobrado: {formato_pesos(self.__costo)}")
            return self.generar_factura()
        finally:
            logger.info(f"Intento de procesar reserva #{self.id} finalizado "
                        f"(estado: {self.__estado})")

    def generar_factura(self):
        """Devuelve un texto con el resumen de cobro de la reserva."""
        return (
            f"  FACTURA Reserva #{self.id}\n"
            f"  Cliente:   {self.__cliente.nombre} (Doc. {self.__cliente.documento})\n"
            f"  Servicio:  {self.__servicio.nombre}\n"
            f"  Duración:  {self.__duracion} {self.__servicio.unidad()}(s)\n"
            f"  Impuesto:  {self.__impuesto}% | Descuento: {self.__descuento}\n"
            f"  TOTAL:     {formato_pesos(self.__costo)}"
        )

    # ---------------- Métodos obligatorios de Entidad ----------------

    def validar(self):
        """Revisa que la reserva siga teniendo cliente y servicio válidos."""
        self._validar_objetos(self.__cliente, self.__servicio)
        return True

    def describir(self):
        costo = formato_pesos(self.__costo) if self.__costo is not None else "sin calcular"
        texto = (f"Reserva #{self.id}: {self.__cliente.nombre} -> {self.__servicio.nombre} | "
                 f"{self.__duracion} {self.__servicio.unidad()}(s) | {costo} | {self.__estado}")
        if self.__estado == Reserva.CANCELADA:
            texto += f" ({self.__motivo_cancelacion})"
        return texto
