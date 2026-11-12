"""
Prueba del Paso 5: gestor del sistema y listas internas.
Ejecutar desde la raíz del proyecto:  python -m pruebas.prueba_paso5
(La simulación completa está en main.py:  python main.py)
"""

from src.gestor.sistema import SistemaSoftwareFJ
from src.servicios.reserva_sala import ReservaSala

print("=== PRUEBA PASO 5: GESTOR DEL SISTEMA ===")
sistema = SistemaSoftwareFJ()

print("\n1. Registrar cliente válido")
sistema.registrar_cliente("Laura Díaz", "1012345678", "laura@correo.com", "3112223344")

print("\n2. Registrar el mismo documento otra vez (debe fallar)")
sistema.registrar_cliente("Laura Copia", "1012345678", "copia@correo.com", "3112223344")

print("\n3. Registrar sala")
sistema.registrar_servicio(ReservaSala, "Sala Norte", 40000, 6)

print("\n4. Reserva válida")
reserva = sistema.crear_reserva("1012345678", "Sala Norte", 2, asistentes=5)

print("\n5. Error inesperado (tipo de servicio que no es una clase): tampoco detiene el sistema")
sistema.registrar_servicio(None, "Algo", 1000)

print("\n6. Procesar la reserva")
sistema.procesar_reserva(reserva.id)

sistema.mostrar_resumen()
