"""
Prueba del Paso 2: clase abstracta Entidad y clase Cliente.
Ejecutar desde la raíz del proyecto:  python -m pruebas.prueba_paso2
"""

from src.modelos.entidad import Entidad
from src.modelos.cliente import Cliente
from src.excepciones.excepciones import SoftwareFJError
from src.utils.logger import logger

print("=== PRUEBA PASO 2: ENTIDAD Y CLIENTE ===\n")

# Prueba 1: la clase abstracta no se puede instanciar
try:
    Entidad()
except TypeError as e:
    logger.error(e, "Instanciar Entidad abstracta")
    print(f"1. Entidad es abstracta, no se puede crear: {e}\n")

# Lista de clientes a registrar: válidos e inválidos
datos_clientes = [
    ("oscar blanco", "1098765432", "Oscar@Correo.com", "3101234567"),   # Válido
    ("Ana María Pérez", "52123456", "ana.perez@unad.edu.co", "3209876543"),  # Válido
    ("Luis", "10A9876", "luis@correo.com", "3001112233"),              # Documento con letras
    ("Carlos Ruiz", "80123456", "carlos@correo", "3001112233"),        # Correo sin dominio
    ("", "80123456", "x@correo.com", "3001112233"),                    # Nombre vacío
    ("Marta Gómez", "41234567", "marta@correo.com", "6012345"),        # Teléfono fijo, no celular
]

clientes = []  # Lista interna de clientes registrados correctamente

# Prueba 2: registro de clientes con try/except/else
for i, datos in enumerate(datos_clientes, start=2):
    try:
        cliente = Cliente(*datos)
    except SoftwareFJError as e:
        logger.error(e, "Registro de cliente")
        print(f"{i}. RECHAZADO -> {e}")
    else:
        clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.nombre} (id {cliente.id})")
        print(f"{i}. REGISTRADO -> {cliente}")

# Prueba 3: modificar un dato con un valor inválido (el valor anterior se conserva)
print()
cliente = clientes[0]
try:
    cliente.correo = "correo-malo"
except SoftwareFJError as e:
    logger.error(e, "Actualizar correo")
    print(f"8. No se cambió el correo: {e}")
finally:
    print(f"   Correo actual sigue siendo: {cliente.correo}")

# Prueba 4: encapsulación, el atributo privado no se accede directamente
try:
    print(cliente.__telefono)
except AttributeError:
    print(f"9. El teléfono es privado; solo se ve enmascarado: {cliente.telefono}")

# Prueba 5: validar() revisa todos los datos
print(f"10. Validación completa del cliente #{cliente.id}: {cliente.validar()}")

print(f"\nTotal registrados: {len(clientes)} de {len(datos_clientes)}. El programa siguió funcionando.")
