"""
Prueba del Paso 1: excepciones personalizadas y logger.
Ejecutar desde la raíz del proyecto:  python -m pruebas.prueba_paso1
"""

from src.excepciones.excepciones import (
    SoftwareFJError, DatoInvalidoError, ParametroFaltanteError,
    ServicioNoDisponibleError, OperacionNoPermitidaError,
)
from src.utils.logger import logger, ARCHIVO_LOG

print("=== PRUEBA PASO 1: EXCEPCIONES Y LOGGER ===\n")

# Prueba 1: evento normal
logger.info("Inicio de prueba del Paso 1")
print("1. Evento INFO registrado")

# Prueba 2: try/except con excepción personalizada
try:
    raise DatoInvalidoError("correo", "oscar@", "formato de correo incorrecto")
except DatoInvalidoError as e:
    logger.error(e, "Registro de cliente")
    print(f"2. Capturado: {e}")

# Prueba 3: try/except/else (else solo corre si NO hubo error)
try:
    valor = 100 * 2
except Exception as e:
    logger.error(e)
else:
    logger.info(f"Cálculo correcto: {valor}")
    print(f"3. Sin error, entró al else: {valor}")

# Prueba 4: encadenamiento de excepciones (raise ... from)
try:
    try:
        int("abc")  # Error original de Python
    except ValueError as original:
        raise DatoInvalidoError("duración", "abc", "debe ser numérico") from original
except SoftwareFJError as e:
    logger.error(e, "Crear reserva")
    print(f"4. Encadenada: {e}  <- causa: {e.__cause__}")

# Prueba 5: try/except/finally (finally siempre se ejecuta)
try:
    raise OperacionNoPermitidaError("cancelar", "CANCELADA")
except OperacionNoPermitidaError as e:
    logger.error(e, "Cancelar reserva")
    print(f"5. Capturado: {e}")
finally:
    print("   finally ejecutado")

# Prueba 6: capturar por la clase base (polimorfismo de excepciones)
for error in (ParametroFaltanteError("nombre"), ServicioNoDisponibleError("Sala VIP")):
    try:
        raise error
    except SoftwareFJError as e:
        logger.error(e)
        print(f"6. Capturado con la clase base: {e}")

print(f"\nEl programa siguió funcionando. Revisa el log en: {ARCHIVO_LOG}")
