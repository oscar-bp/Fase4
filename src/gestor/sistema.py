"""
Módulo: sistema.py
Descripción: Gestor central de Software FJ. Guarda clientes, servicios y
reservas en listas internas (sin base de datos) y ofrece las operaciones
del sistema. Cada operación pasa por un ejecutor seguro que captura los
errores, los registra en el log y permite que el programa siga funcionando.
"""

from src.modelos.cliente import Cliente
from src.servicios.servicio import formato_pesos
from src.reservas.reserva import Reserva
from src.excepciones.excepciones import SoftwareFJError, DatoInvalidoError
from src.utils.logger import logger


class SistemaSoftwareFJ:
    """Administra las listas internas y las operaciones del sistema."""

    def __init__(self):
        # Listas internas: reemplazan a la base de datos
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        # Contadores para el resumen final
        self.__exitos = 0
        self.__errores = 0
        logger.info("=== Sistema Software FJ iniciado ===")

    # ---------------- Ejecutor seguro (núcleo de la estabilidad) ----------------

    def _ejecutar(self, descripcion, accion):
        """
        Ejecuta cualquier operación sin que el sistema se caiga:
          - try:     ejecuta la acción
          - except:  errores propios del sistema (SoftwareFJError) o inesperados (Exception)
          - else:    cuenta el éxito y lo registra
          - finally: siempre muestra el resultado de la operación
        Devuelve el resultado de la acción, o None si falló.
        """
        resultado, exito = None, False
        try:
            resultado = accion()
        except SoftwareFJError as e:
            self.__errores += 1
            logger.error(e, descripcion)
            print(f"   ✗ ERROR: {e}")
            if e.__cause__:
                print(f"     Causa: {e.__cause__}")
        except Exception as e:
            # Red de seguridad: cualquier error no previsto tampoco detiene el sistema
            self.__errores += 1
            logger.error(e, f"{descripcion} (error inesperado)")
            print(f"   ✗ ERROR INESPERADO: {type(e).__name__}: {e}")
        else:
            exito = True
            self.__exitos += 1
            logger.info(f"Operación exitosa: {descripcion}")
        finally:
            print(f"   -> {'Completada' if exito else 'Fallida, el sistema continúa'}")
        return resultado

    # ---------------- Clientes ----------------

    def registrar_cliente(self, nombre, documento, correo, telefono):
        """Registra un cliente nuevo; no permite documentos repetidos."""
        def accion():
            if any(c.documento == str(documento).strip() for c in self.__clientes):
                raise DatoInvalidoError("documento", documento, "ya existe un cliente con ese documento")
            cliente = Cliente(nombre, documento, correo, telefono)
            self.__clientes.append(cliente)
            print(f"   ✓ {cliente}")
            return cliente
        return self._ejecutar(f"Registrar cliente '{nombre}'", accion)

    def buscar_cliente(self, documento):
        """Busca un cliente por documento; lanza excepción si no existe."""
        for cliente in self.__clientes:
            if cliente.documento == str(documento):
                return cliente
        raise DatoInvalidoError("documento", documento, "no hay un cliente registrado con ese documento")

    # ---------------- Servicios ----------------

    def registrar_servicio(self, clase_servicio, *datos):
        """Crea un servicio de cualquier tipo (Sala, Equipo, Asesoría) y lo agrega a la lista."""
        def accion():
            servicio = clase_servicio(*datos)
            self.__servicios.append(servicio)
            print(f"   ✓ {servicio}")
            return servicio
        # getattr evita un error si llega algo que no es una clase (ej. None)
        tipo = getattr(clase_servicio, "__name__", str(clase_servicio))
        return self._ejecutar(f"Registrar servicio {tipo}", accion)

    def buscar_servicio(self, nombre):
        """Busca un servicio por nombre (sin importar mayúsculas)."""
        for servicio in self.__servicios:
            if servicio.nombre.lower() == str(nombre).lower():
                return servicio
        raise DatoInvalidoError("servicio", nombre, "no existe un servicio con ese nombre")

    def cambiar_disponibilidad(self, nombre_servicio, disponible):
        """Habilita o deshabilita un servicio (ej. por mantenimiento)."""
        def accion():
            servicio = self.buscar_servicio(nombre_servicio)
            servicio.habilitar() if disponible else servicio.deshabilitar()
            print(f"   ✓ {servicio}")
            return servicio
        estado = "Habilitar" if disponible else "Deshabilitar"
        return self._ejecutar(f"{estado} servicio '{nombre_servicio}'", accion)

    # ---------------- Reservas ----------------

    def crear_reserva(self, documento, nombre_servicio, duracion, impuesto=19, descuento=0, **opciones):
        """Crea una reserva buscando el cliente y el servicio en las listas internas, y la confirma."""
        def accion():
            cliente = self.buscar_cliente(documento)
            servicio = self.buscar_servicio(nombre_servicio)
            reserva = Reserva(cliente, servicio, duracion, impuesto, descuento, **opciones)
            # Se agrega a la lista aunque la confirmación falle, para dejar trazabilidad
            self.__reservas.append(reserva)
            reserva.confirmar()
            print(f"   ✓ {reserva}")
            return reserva
        return self._ejecutar(f"Crear reserva ({documento} -> {nombre_servicio})", accion)

    def buscar_reserva(self, id_reserva):
        """Busca una reserva por su id."""
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        raise DatoInvalidoError("id de reserva", id_reserva, "no existe una reserva con ese id")

    def cancelar_reserva(self, id_reserva, motivo="Sin motivo"):
        """Cancela una reserva existente."""
        def accion():
            reserva = self.buscar_reserva(id_reserva)
            reserva.cancelar(motivo)
            print(f"   ✓ {reserva}")
            return reserva
        return self._ejecutar(f"Cancelar reserva #{id_reserva}", accion)

    def procesar_reserva(self, id_reserva):
        """Procesa (cobra) una reserva confirmada y muestra su factura."""
        def accion():
            reserva = self.buscar_reserva(id_reserva)
            factura = reserva.procesar()
            print(factura)
            return reserva
        return self._ejecutar(f"Procesar reserva #{id_reserva}", accion)

    # ---------------- Reportes ----------------

    def mostrar_resumen(self):
        """Muestra el contenido de las listas internas y las estadísticas de la ejecución."""
        print("\n" + "=" * 70)
        print("RESUMEN DEL SISTEMA")
        print("=" * 70)

        print(f"\nClientes registrados ({len(self.__clientes)}):")
        for cliente in self.__clientes:
            print(f"   {cliente}")

        print(f"\nServicios registrados ({len(self.__servicios)}):")
        for servicio in self.__servicios:
            print(f"   {servicio}")

        print(f"\nReservas ({len(self.__reservas)}):")
        for reserva in self.__reservas:
            print(f"   {reserva}")

        # Total facturado: solo cuentan las reservas procesadas
        total = sum(r.costo for r in self.__reservas if r.estado == Reserva.PROCESADA)
        print(f"\nTotal facturado: {formato_pesos(total)}")
        print(f"Operaciones exitosas: {self.__exitos} | Operaciones con error: {self.__errores}")
        print("El sistema terminó sin interrupciones. Detalle en logs/eventos.log")
        logger.info(f"=== Fin de ejecución: {self.__exitos} exitosas, {self.__errores} con error ===")
