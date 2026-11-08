"""
Módulo: logger.py
Descripción: Registra eventos y errores del sistema en el archivo logs/eventos.log.
No usa base de datos: solo escribe en un archivo de texto plano.
Si por algún motivo no se puede escribir el log, el sistema NO se detiene.
"""

import os
from datetime import datetime

# Ruta de la carpeta logs (en la raíz del proyecto, dos niveles arriba de este archivo)
_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_LOGS = os.path.join(_RAIZ, "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "eventos.log")


class Logger:
    """Clase encargada de escribir los eventos y errores en el archivo de logs."""

    # Niveles permitidos para clasificar cada registro
    NIVELES = ("INFO", "ADVERTENCIA", "ERROR")

    def __init__(self, ruta=ARCHIVO_LOG):
        self.__ruta = ruta  # Atributo privado: ruta del archivo de log
        # Crea la carpeta logs si no existe
        os.makedirs(os.path.dirname(self.__ruta), exist_ok=True)

    def _escribir(self, nivel, mensaje):
        """Escribe una línea en el log con fecha, hora y nivel."""
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"{fecha} | {nivel:<11} | {mensaje}\n"
        archivo = None
        try:
            # Abre el archivo en modo 'a' (agregar) para no borrar registros anteriores
            archivo = open(self.__ruta, "a", encoding="utf-8")
            archivo.write(linea)
        except OSError as e:
            # Si falla la escritura, se avisa por consola pero el programa sigue
            print(f"[AVISO] No se pudo escribir en el log: {e}")
        finally:
            # finally: siempre se cierra el archivo, haya error o no
            if archivo:
                archivo.close()

    def info(self, mensaje):
        """Registra un evento normal (operación exitosa)."""
        self._escribir("INFO", mensaje)

    def advertencia(self, mensaje):
        """Registra una situación que no es error pero merece atención."""
        self._escribir("ADVERTENCIA", mensaje)

    def error(self, excepcion, contexto=""):
        """
        Registra un error. Si la excepción viene encadenada (raise ... from),
        también registra la causa original para saber de dónde vino.
        """
        texto = f"{contexto} -> {type(excepcion).__name__}: {excepcion}" if contexto \
            else f"{type(excepcion).__name__}: {excepcion}"
        # __cause__ guarda la excepción original cuando se usa 'raise ... from'
        if excepcion.__cause__ is not None:
            causa = excepcion.__cause__
            texto += f" | Causa: {type(causa).__name__}: {causa}"
        self._escribir("ERROR", texto)


# Instancia única que usan todos los módulos del proyecto
logger = Logger()
