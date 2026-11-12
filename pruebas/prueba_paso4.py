"""
Prueba del Paso 4: clase Reserva (confirmar, cancelar, procesar).
Ejecutar desde la raíz del proyecto:  python -m pruebas.prueba_paso4
"""

from src.modelos.cliente import Cliente
from src.servicios.reserva_sala import ReservaSala
from src.servicios.alquiler_equipo import AlquilerEquipo
from src.servicios.asesoria import Asesoria
from src.reservas.reserva import Reserva
from src.excepciones.excepciones import SoftwareFJError
from src.utils.logger import logger


def ejecutar(numero, descripcion, accion):
    """Ejecuta una acción de prueba; si falla, registra el error y continúa."""
    try:
        resultado = accion()
    except SoftwareFJError as e:
        logger.error(e, descripcion)
        causa = f"\n      causa: {e.__cause__}" if e.__cause__ else ""
        print(f"{numero}. ERROR ({descripcion}) -> {e}{causa}")
        return None
    else:
        print(f"{numero}. OK ({descripcion})")
        return resultado


print("=== PRUEBA PASO 4: RESERVAS ===\n")

# Datos base para las pruebas
oscar = Cliente("Oscar Blanco", "1098765432", "oscar@correo.com", "3101234567")
ana = Cliente("Ana Pérez", "52123456", "ana@correo.com", "3209876543")
sala = ReservaSala("Sala Ejecutiva", 50000, 10)
equipo = AlquilerEquipo("Portátil Lenovo", 35000, 5)
asesoria = Asesoria("Asesoría Web", 80000, "Desarrollo web")

# 1. Reserva válida: crear, confirmar y procesar
r1 = ejecutar(1, "Crear reserva de sala", lambda: Reserva(oscar, sala, 3, asistentes=8))
ejecutar(2, "Confirmar reserva de sala", r1.confirmar)
factura = ejecutar(3, "Procesar reserva de sala", r1.procesar)
print(factura)

# 2. Reserva con cupón y nivel avanzado
r2 = ejecutar(4, "Crear asesoría avanzada con cupón",
              lambda: Reserva(ana, asesoria, 2, descuento="FJ20", nivel="avanzado"))
ejecutar(5, "Confirmar asesoría", r2.confirmar)

# 3. Cliente inválido (texto en lugar de objeto Cliente)
ejecutar(6, "Crear reserva con cliente inválido", lambda: Reserva("Pedro", sala, 2))

# 4. Duración fuera de rango: el error del servicio se encadena al de la reserva
r3 = ejecutar(7, "Crear reserva de equipo por 40 días", lambda: Reserva(ana, equipo, 40))
ejecutar(8, "Confirmar reserva de 40 días", r3.confirmar)
print(f"   Estado tras el error: {r3.estado} (no cambió)")

# 5. Servicio no disponible al confirmar
equipo.deshabilitar()
r4 = ejecutar(9, "Crear reserva de equipo", lambda: Reserva(oscar, equipo, 2, cantidad=2))
ejecutar(10, "Confirmar con equipo no disponible", r4.confirmar)
equipo.habilitar()

# 6. Operaciones no permitidas según el estado
ejecutar(11, "Procesar reserva PENDIENTE", r4.procesar)
ejecutar(12, "Cancelar reserva de asesoría", lambda: r2.cancelar("Cliente reprogramó"))
ejecutar(13, "Cancelar otra vez la misma reserva", lambda: r2.cancelar("Duplicado"))
ejecutar(14, "Cancelar reserva ya PROCESADA", lambda: r1.cancelar())

# 7. El servicio deja de estar disponible después de confirmar
r5 = ejecutar(15, "Crear y confirmar sala", lambda: Reserva(ana, sala, 2, asistentes=4))
ejecutar(16, "Confirmar sala", r5.confirmar)
sala.deshabilitar()
ejecutar(17, "Procesar con sala en mantenimiento", r5.procesar)
sala.habilitar()

# Resumen final
print("\n--- Estado final de las reservas ---")
for reserva in (r1, r2, r3, r4, r5):
    print(f"   {reserva}")

print("\nEl programa siguió funcionando. Revisa logs/eventos.log")
