"""
Prueba del Paso 3: clase abstracta Servicio, servicios especializados y sobrecarga de costos.
Ejecutar desde la raíz del proyecto:  python -m pruebas.prueba_paso3
"""

from src.servicios.servicio import Servicio, formato_pesos
from src.servicios.reserva_sala import ReservaSala
from src.servicios.alquiler_equipo import AlquilerEquipo
from src.servicios.asesoria import Asesoria
from src.excepciones.excepciones import SoftwareFJError
from src.utils.logger import logger

print("=== PRUEBA PASO 3: SERVICIOS ===\n")

# ---------------- 1. Servicio es abstracta ----------------
try:
    Servicio("Genérico", 1000)
except TypeError:
    print("1. Servicio es abstracta: no se puede crear directamente\n")

# ---------------- 2. Creación de servicios válidos e inválidos ----------------
# Cada elemento: (descripción, función que crea el servicio)
intentos = [
    ("Sala válida",       lambda: ReservaSala("Sala Ejecutiva", 50000, 10)),
    ("Equipo válido",     lambda: AlquilerEquipo("Portátil Lenovo", 35000, 5)),
    ("Asesoría válida",   lambda: Asesoria("Asesoría Web", 80000, "Desarrollo web")),
    ("Precio negativo",   lambda: ReservaSala("Sala Mini", -20000, 4)),
    ("Precio con texto",  lambda: AlquilerEquipo("Proyector", "abc", 2)),
    ("Sin especialidad",  lambda: Asesoria("Asesoría Redes", 70000, "")),
    ("Capacidad en cero", lambda: ReservaSala("Sala Vacía", 30000, 0)),
]

servicios = []  # Lista interna de servicios creados correctamente
print("2. Creación de servicios:")
for descripcion, crear in intentos:
    try:
        servicio = crear()
    except SoftwareFJError as e:
        logger.error(e, f"Crear servicio ({descripcion})")
        causa = f"  <- causa: {e.__cause__}" if e.__cause__ else ""
        print(f"   RECHAZADO ({descripcion}) -> {e}{causa}")
    else:
        servicios.append(servicio)
        logger.info(f"Servicio creado: {servicio.nombre}")
        print(f"   CREADO -> {servicio}")

sala, equipo, asesoria = servicios

# ---------------- 3. Polimorfismo: misma llamada, cálculo distinto ----------------
print("\n3. Polimorfismo (calcular_costo(2) en cada servicio):")
for s in servicios:
    print(f"   {s.nombre:<16} 2 {s.unidad()}s -> {formato_pesos(s.calcular_costo(2))}")

# ---------------- 4. Sobrecarga: varias formas de calcular el costo ----------------
print("\n4. Sobrecarga del cálculo (Asesoría Web, 3 horas):")
print(f"   Solo base                   -> {formato_pesos(asesoria.calcular_costo(3))}")
print(f"   Con IVA 19%                 -> {formato_pesos(asesoria.calcular_costo(3, impuesto=19))}")
print(f"   IVA 19% + 10% descuento     -> {formato_pesos(asesoria.calcular_costo(3, 19, 10))}")
print(f"   IVA 19% + cupón 'UNAD10'    -> {formato_pesos(asesoria.calcular_costo(3, 19, 'UNAD10'))}")
print(f"   IVA 19% + nivel avanzado    -> {formato_pesos(asesoria.calcular_costo(3, 19, nivel='avanzado'))}")
print(f"   Equipo: 3 días, 2 unidades  -> {formato_pesos(equipo.calcular_costo(3, 19, cantidad=2))}")

# ---------------- 5. Cálculos con errores (el programa no se detiene) ----------------
print("\n5. Cálculos inválidos:")
casos_error = [
    ("Sala por 20 horas",         lambda: sala.calcular_costo(20)),
    ("Sala con 15 asistentes",    lambda: sala.calcular_costo(2, asistentes=15)),
    ("Duración con texto",        lambda: equipo.calcular_costo("tres")),
    ("Descuento de 150%",         lambda: asesoria.calcular_costo(2, 19, 150)),
    ("Cupón que no existe",       lambda: asesoria.calcular_costo(2, 19, "GRATIS")),
    ("Nivel inexistente",         lambda: asesoria.calcular_costo(2, nivel="experto")),
    ("Más equipos de los que hay", lambda: equipo.calcular_costo(2, cantidad=8)),
]
for descripcion, calcular in casos_error:
    try:
        calcular()
    except SoftwareFJError as e:
        logger.error(e, f"Cálculo de costo ({descripcion})")
        print(f"   ERROR ({descripcion}) -> {e}")

# ---------------- 6. Servicio no disponible ----------------
print("\n6. Disponibilidad:")
sala.deshabilitar()
try:
    sala.verificar_disponibilidad()
except SoftwareFJError as e:
    logger.error(e, "Verificar disponibilidad")
    print(f"   {e}")
finally:
    sala.habilitar()
    print(f"   Sala habilitada de nuevo -> {sala.disponible}")

print(f"\nServicios creados: {len(servicios)} de {len(intentos)}. El programa siguió funcionando.")
