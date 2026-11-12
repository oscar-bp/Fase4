"""
Archivo: main.py
Descripción: Punto de entrada del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de Software FJ. Simula operaciones completas, válidas
e inválidas, para demostrar que el sistema registra cada error en el log
y sigue funcionando sin detenerse.

Ejecutar desde la raíz del proyecto:  python main.py
"""

from src.gestor.sistema import SistemaSoftwareFJ
from src.servicios.reserva_sala import ReservaSala
from src.servicios.alquiler_equipo import AlquilerEquipo
from src.servicios.asesoria import Asesoria

# Contador para numerar cada operación en pantalla
numero = 0


def operacion(titulo):
    """Imprime el encabezado numerado de cada operación."""
    global numero
    numero += 1
    print(f"\n[{numero:02d}] {titulo}")


def main():
    print("=" * 70)
    print("SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 70)

    sistema = SistemaSoftwareFJ()

    # ---------------- Registro de clientes ----------------
    operacion("Registrar cliente válido")
    sistema.registrar_cliente("Oscar Blanco", "1098765432", "oscar@correo.com", "3101234567")

    operacion("Registrar cliente válido")
    sistema.registrar_cliente("Ana María Pérez", "52123456", "ana.perez@correo.com", "3209876543")

    operacion("Registrar cliente con correo inválido")
    sistema.registrar_cliente("Carlos Ruiz", "80123456", "carlos@correo", "3001112233")

    operacion("Registrar cliente con documento repetido")
    sistema.registrar_cliente("Pedro Gómez", "52123456", "pedro@correo.com", "3157778899")

    # ---------------- Registro de servicios ----------------
    operacion("Registrar servicio: sala")
    sistema.registrar_servicio(ReservaSala, "Sala Ejecutiva", 50000, 10)

    operacion("Registrar servicio: alquiler de equipo")
    sistema.registrar_servicio(AlquilerEquipo, "Portátil Lenovo", 35000, 5)

    operacion("Registrar servicio: asesoría")
    sistema.registrar_servicio(Asesoria, "Asesoría Web", 80000, "Desarrollo web")

    operacion("Registrar servicio con precio negativo")
    sistema.registrar_servicio(ReservaSala, "Sala Mini", -20000, 4)

    operacion("Registrar servicio con precio en texto (error encadenado)")
    sistema.registrar_servicio(AlquilerEquipo, "Proyector Epson", "abc", 2)

    # ---------------- Reservas exitosas ----------------
    operacion("Reservar sala 3 horas para 8 personas")
    r_sala = sistema.crear_reserva("1098765432", "Sala Ejecutiva", 3, asistentes=8)

    operacion("Reservar asesoría avanzada con cupón FJ20")
    r_asesoria = sistema.crear_reserva("52123456", "Asesoría Web", 2, descuento="FJ20", nivel="avanzado")

    operacion("Reservar 2 portátiles por 5 días con 10% de descuento")
    r_equipo = sistema.crear_reserva("52123456", "Portátil Lenovo", 5, descuento=10, cantidad=2)

    # ---------------- Reservas con errores ----------------
    operacion("Reservar con cliente no registrado")
    sistema.crear_reserva("99999999", "Sala Ejecutiva", 2)

    operacion("Reservar servicio inexistente")
    sistema.crear_reserva("1098765432", "Sala VIP", 2)

    operacion("Reservar sala para 15 personas (supera capacidad)")
    sistema.crear_reserva("1098765432", "Sala Ejecutiva", 2, asistentes=15)

    operacion("Reservar con descuento de 150% (cálculo inconsistente)")
    sistema.crear_reserva("1098765432", "Asesoría Web", 2, descuento=150)

    operacion("Deshabilitar portátiles por mantenimiento")
    sistema.cambiar_disponibilidad("Portátil Lenovo", False)

    operacion("Reservar portátil no disponible")
    sistema.crear_reserva("1098765432", "Portátil Lenovo", 2)

    operacion("Habilitar portátiles de nuevo")
    sistema.cambiar_disponibilidad("Portátil Lenovo", True)

    # ---------------- Procesamiento y cancelación ----------------
    if r_sala:
        operacion("Procesar reserva de sala")
        sistema.procesar_reserva(r_sala.id)

        operacion("Cancelar reserva ya procesada (no permitido)")
        sistema.cancelar_reserva(r_sala.id, "Cambio de planes")

    if r_asesoria:
        operacion("Cancelar reserva de asesoría")
        sistema.cancelar_reserva(r_asesoria.id, "Cliente reprogramó")

        operacion("Procesar reserva cancelada (no permitido)")
        sistema.procesar_reserva(r_asesoria.id)

    if r_equipo:
        operacion("Procesar reserva de portátiles")
        sistema.procesar_reserva(r_equipo.id)

    operacion("Procesar reserva inexistente")
    sistema.procesar_reserva(999)

    # ---------------- Resumen final ----------------
    sistema.mostrar_resumen()


# Solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    main()
