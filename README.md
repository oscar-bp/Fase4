# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Universidad Nacional Abierta y a Distancia – UNAD**
Curso: Programación (213023) – Fase 4: Prácticas simuladas

Sistema orientado a objetos, **sin base de datos**, que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías) y reservas. Aplica abstracción,
herencia, polimorfismo, encapsulación y manejo avanzado de excepciones. Todos los
eventos y errores se registran en un archivo de logs y el programa sigue funcionando
aunque ocurran errores.

---

## Integrantes y reparto

| Bloque | Contenido | Responsable | Estado |
|---|---|---|---|
| 1 | Excepciones personalizadas + logger + README | Oscar Blanco | ✅ Terminado |
| 2 | Clase abstracta `Entidad` + clase `Cliente` | Oscar Blanco | ✅ Terminado |
| 3 | Clase abstracta `Servicio` + 3 servicios + sobrecarga de costos | Oscar Blanco | ✅ Terminado |
| 4 | Clase `Reserva` (confirmar, cancelar, procesar) | Oscar Blanco | ✅ Terminado |
| 5 | Gestor del sistema + `main.py` con las 10 operaciones | Oscar Blanco | ✅ Terminado |

> El plazo para vincularse al trabajo colaborativo venció el **10 de noviembre de 2026** y espere hasta el **12 de noviembre**.
> Al no reportarse más integrantes, el proyecto se desarrolla de forma individual.

## Estructura del proyecto

```
Fase4/
├── main.py                     # Simulación de las 10+ operaciones (Bloque 5)
├── README.md                   # Este archivo
├── .gitignore                  # Excluye caché de Python y logs
├── logs/
│   └── eventos.log             # Se crea solo al ejecutar (no se sube)
├── pruebas/
│   ├── prueba_paso1.py         # Prueba de excepciones y logger
│   └── prueba_pasoN.py         # Cada bloque agrega su propia prueba
└── src/
    ├── excepciones/
    │   └── excepciones.py      # Excepciones personalizadas (Bloque 1)
    ├── utils/
    │   └── logger.py           # Registro de eventos y errores (Bloque 1)
    ├── modelos/
    │   ├── entidad.py          # Clase abstracta Entidad (Bloque 2)
    │   └── cliente.py          # Cliente con validaciones (Bloque 2)
    ├── servicios/
    │   ├── servicio.py         # Clase abstracta Servicio (Bloque 3)
    │   ├── reserva_sala.py     # Servicio 1 (Bloque 3)
    │   ├── alquiler_equipo.py  # Servicio 2 (Bloque 3)
    │   └── asesoria.py         # Servicio 3 (Bloque 3)
    ├── reservas/
    │   └── reserva.py          # Clase Reserva (Bloque 4)
    └── gestor/
        └── sistema.py          # Listas internas del sistema (Bloque 5)
```

Cada carpeta dentro de `src/` lleva un archivo `__init__.py` (puede tener solo un
comentario) para que Python la reconozca como paquete.

---

## Cómo ejecutar

Requisitos: **Python 3.10 o superior**. No necesita librerías externas.

Todos los comandos se ejecutan **desde la carpeta raíz** del proyecto (`Fase4/`):

```bash
# Probar un bloque específico
python -m pruebas.prueba_paso1

# Ejecutar el sistema completo (cuando esté el Bloque 5)
python main.py
```

Después de ejecutar, revisa `logs/eventos.log` para ver los eventos y errores registrados.

---

## Reglas de trabajo para todos

1. **Usar las excepciones y el logger del Bloque 1.** No crear excepciones sueltas ni
   escribir logs por otro lado:
   ```python
   from src.excepciones.excepciones import DatoInvalidoError, ParametroFaltanteError
   from src.utils.logger import logger

   logger.info("Cliente registrado correctamente")
   logger.error(error, "Registro de cliente")
   ```
   Si necesitas una excepción nueva, agrégala en `excepciones.py` heredando de
   `SoftwareFJError` o de una de sus hijas.

2. **Comentar el código.** Cada archivo inicia con un bloque que diga qué hace el módulo,
   y cada clase y método lleva un comentario o docstring breve.

3. **Probar antes de subir.** Cada bloque agrega su archivo `pruebas/prueba_pasoN.py`
   y lo ejecuta para verificar que funciona.

4. **Atributos privados** con doble guion bajo (`self.__nombre`) y acceso mediante
   `@property` para cumplir la encapsulación.

5. **Nombres en español** y en formato `snake_case` para variables, funciones y archivos;
   `PascalCase` para clases.

6. **Commits propios y claros.** Cada integrante sube su trabajo con su cuenta:
   ```bash
   git pull
   git add .
   git commit -m "Bloque 2: clase Cliente con validaciones"
   git push
   ```
   Hacer `git pull` antes de empezar a trabajar para tener la última versión.

---

## Excepciones disponibles (Bloque 1)

| Excepción | Código | Cuándo usarla |
|---|---|---|
| `SoftwareFJError` | ERR-000 | Base de todas; sirve para capturar cualquier error del sistema |
| `DatoInvalidoError` | ERR-DATO | Un dato no cumple el formato (correo, teléfono, documento…) |
| `ParametroFaltanteError` | ERR-FALTA | Falta un dato obligatorio o viene vacío |
| `ServicioError` | ERR-SERV | Error general de servicios |
| `ServicioNoDisponibleError` | ERR-NODISP | Se intenta reservar un servicio no disponible |
| `CalculoInconsistenteError` | ERR-CALC | Un costo da negativo o imposible |
| `ReservaError` | ERR-RES | Error general de reservas |
| `OperacionNoPermitidaError` | ERR-OPER | Acción inválida según el estado de la reserva |

---

## Requisitos del enunciado que cubre el proyecto

- [x] Excepciones personalizadas
- [x] `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from`)
- [x] Archivo de logs con eventos y errores
- [x] Clase abstracta que represente entidades generales
- [x] Clase `Cliente` con validaciones y encapsulación
- [x] Clase abstracta `Servicio` y tres servicios especializados
- [x] Métodos sobrecargados (costo con impuestos, descuentos o parámetros opcionales)
- [x] Clase `Reserva` con confirmación, cancelación y procesamiento
- [x] Simulación de al menos 10 operaciones (válidas e inválidas)
