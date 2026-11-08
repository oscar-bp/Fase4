"""
Módulo: excepciones.py
Descripción: Define las excepciones personalizadas del sistema Software FJ.
Todas heredan de SoftwareFJError, así se pueden capturar de forma general
o de forma específica según el tipo de error.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema. Todas las demás heredan de esta."""

    def __init__(self, mensaje, codigo="ERR-000"):
        # Guarda el mensaje y un código para identificar el tipo de error en los logs
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        # Formato legible: [código] mensaje
        return f"[{self.codigo}] {self.mensaje}"


# ---------------------------------------------------------------
# Errores de datos (validaciones de clientes y parámetros)
# ---------------------------------------------------------------

class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato no cumple el formato o las reglas (ej. correo mal escrito)."""

    def __init__(self, campo, valor, detalle="valor no válido"):
        self.campo = campo   # Nombre del campo que falló
        self.valor = valor   # Valor que se intentó asignar
        super().__init__(f"Campo '{campo}' con valor '{valor}': {detalle}", "ERR-DATO")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio (vacío o None)."""

    def __init__(self, parametro):
        self.parametro = parametro
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'", "ERR-FALTA")


# ---------------------------------------------------------------
# Errores de servicios
# ---------------------------------------------------------------

class ServicioError(SoftwareFJError):
    """Error general relacionado con la creación o uso de servicios."""

    def __init__(self, mensaje, codigo="ERR-SERV"):
        super().__init__(mensaje, codigo)


class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, nombre_servicio):
        self.nombre_servicio = nombre_servicio
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "ERR-NODISP")


class CalculoInconsistenteError(ServicioError):
    """Se lanza cuando un cálculo de costo da un resultado imposible (ej. negativo)."""

    def __init__(self, detalle):
        super().__init__(f"Cálculo inconsistente: {detalle}", "ERR-CALC")


# ---------------------------------------------------------------
# Errores de reservas
# ---------------------------------------------------------------

class ReservaError(SoftwareFJError):
    """Error general en el proceso de una reserva."""

    def __init__(self, mensaje, codigo="ERR-RES"):
        super().__init__(mensaje, codigo)


class OperacionNoPermitidaError(ReservaError):
    """Se lanza al intentar una acción inválida según el estado (ej. cancelar una reserva ya cancelada)."""

    def __init__(self, operacion, estado_actual):
        self.operacion = operacion
        self.estado_actual = estado_actual
        super().__init__(
            f"No se puede '{operacion}' una reserva en estado '{estado_actual}'",
            "ERR-OPER",
        )
