"""
╔══════════════════════════════════════════════════════════════════╗
║          CAFÉ ANDRÓMEDA — Sistema de Gestión de Pedidos          ║
║                    Versión Integrada — 2026                      ║
║              Fundamentos de Programación — Tecmilenio            ║
╚══════════════════════════════════════════════════════════════════╝

DESCRIPCIÓN:
    Aplicación de consola para el registro, consulta, cálculo y
    persistencia de pedidos de la cafetería "Café Andrómeda".
    Integra todos los fundamentos del curso: entradas/salidas,
    condicionales, ciclos, funciones, listas, diccionarios, tuplas,
    manejo de excepciones y archivos.

AUTOR  : [Roberto Y. Castellanos Eguia]
FECHA  : Mayo 2026
"""

import json
import os
import datetime

# ─────────────────────────────────────────────────────────────────
# CONSTANTES  (tuplas — valores inmutables con propósito claro)
# ─────────────────────────────────────────────────────────────────

# Tupla del menú de productos disponibles: (nombre, precio_unitario)
MENU_PRODUCTOS: tuple = (
    ("Café Americano",    35.00),
    ("Café Latte",        45.00),
    ("Cappuccino",        48.00),
    ("Café Frío",         52.00),
    ("Té Negro",          30.00),
    ("Té Verde",          30.00),
    ("Chocolate Caliente", 40.00),
    ("Brownie",           35.00),
    ("Croissant",         28.00),
    ("Cheesecake",        55.00),
)

# Tupla de opciones válidas del menú principal
OPCIONES_MENU: tuple = ("1", "2", "3", "4", "5", "6")

# Archivo de persistencia
ARCHIVO_PEDIDOS: str = "pedidos.json"

# Separador visual reutilizable
LINEA: str = "─" * 60


# ─────────────────────────────────────────────────────────────────
# UTILIDADES DE PRESENTACIÓN
# ─────────────────────────────────────────────────────────────────

def limpiar_pantalla() -> None:
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_encabezado(titulo: str) -> None:
    """Imprime un encabezado formateado con el título indicado."""
    print("\n" + LINEA)
    print(f"  ☕  CAFÉ ANDRÓMEDA  |  {titulo}")
    print(LINEA)


def pausar() -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presiona Enter para continuar...")


# ─────────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────────

def mostrar_menu_principal() -> None:
    """Despliega el menú principal de opciones del sistema."""
    imprimir_encabezado("Menú Principal")
    print("""
  [1]  Registrar pedido
  [2]  Consultar pedidos registrados
  [3]  Mostrar total acumulado
  [4]  Guardar pedidos en archivo
  [5]  Leer pedidos desde archivo
  [6]  Salir del sistema
""")
    print(LINEA)


def obtener_opcion() -> str:
    """
    Solicita y valida la opción del menú principal.

    Returns:
        str: Opción válida seleccionada por el usuario.

    Raises:
        ValueError: Si la entrada está fuera del rango permitido.
    """
    opcion = input("  Selecciona una opción: ").strip()
    if opcion not in OPCIONES_MENU:
        raise ValueError(f"Opción '{opcion}' no válida. Elige entre 1 y 6.")
    return opcion


# ─────────────────────────────────────────────────────────────────
# CATÁLOGO DE PRODUCTOS
# ─────────────────────────────────────────────────────────────────

def mostrar_catalogo() -> None:
    """Muestra en consola el catálogo de productos disponibles."""
    print("\n  Catálogo de Productos:")
    print(f"  {'No.':<5}{'Producto':<25}{'Precio':>10}")
    print("  " + "·" * 40)
    for idx, (nombre, precio) in enumerate(MENU_PRODUCTOS, start=1):
        print(f"  {idx:<5}{nombre:<25}${precio:>8.2f}")
    print("  " + "·" * 40)


# ─────────────────────────────────────────────────────────────────
# REGISTRO DE PEDIDOS
# ─────────────────────────────────────────────────────────────────

def capturar_entero(mensaje: str, minimo: int = 1) -> int:
    """
    Solicita un número entero al usuario con validación estricta.

    Args:
        mensaje (str): Texto que se muestra al usuario.
        minimo  (int): Valor mínimo aceptado (default 1).

    Returns:
        int: Entero válido ingresado por el usuario.

    Raises:
        ValueError: Si la entrada no es un entero o es menor al mínimo.
    """
    valor = input(mensaje).strip()
    if not valor.lstrip("-").isdigit():
        raise ValueError(
            f"Se esperaba un número entero, se recibió: '{valor}'")
    numero = int(valor)
    if numero < minimo:
        raise ValueError(
            f"El valor debe ser al menos {minimo}. Se ingresó: {numero}")
    return numero


def capturar_precio(mensaje: str) -> float:
    """
    Solicita un precio al usuario con validación estricta.

    Args:
        mensaje (str): Texto que se muestra al usuario.

    Returns:
        float: Precio válido mayor a 0.

    Raises:
        ValueError: Si la entrada no es un número o es ≤ 0.
    """
    valor = input(mensaje).strip()
    try:
        precio = float(valor)
    except ValueError as exc:
        raise ValueError(f"Precio no válido. Se recibió: '{valor}'") from exc
    if precio <= 0:
        raise ValueError(
            f"El precio debe ser mayor a cero. Se ingresó: {precio}")
    return precio


def registrar_pedido(pedidos: list) -> None:
    """
    Registra un nuevo pedido en la lista de pedidos.

    El usuario puede elegir un producto del catálogo (precio
    automático) o ingresar un producto personalizado con su precio.
    Se calcula el subtotal y se agrega el pedido como diccionario.

    Args:
        pedidos (list): Lista donde se almacenan los pedidos activos.
    """
    imprimir_encabezado("Registrar Pedido")
    mostrar_catalogo()

    print("\n  ¿Cómo deseas registrar el producto?")
    print("  [A] Seleccionar del catálogo")
    print("  [B] Ingresar producto personalizado")
    modo = input("\n  Opción: ").strip().upper()

    nombre_producto: str = ""
    precio_unitario: float = 0.0

    if modo == "A":
        # ── Selección desde catálogo ──────────────────────────────
        num_producto = capturar_entero(
            f"  Número de producto (1-{len(MENU_PRODUCTOS)}): ",
            minimo=1
        )
        if num_producto > len(MENU_PRODUCTOS):
            raise ValueError(
                f"Número fuera de rango. Elige entre 1 y {len(MENU_PRODUCTOS)}."
            )
        nombre_producto, precio_unitario = MENU_PRODUCTOS[num_producto - 1]

    elif modo == "B":
        # ── Producto personalizado ────────────────────────────────
        nombre_producto = input("  Nombre del producto: ").strip()
        if not nombre_producto:
            raise ValueError("El nombre del producto no puede estar vacío.")
        precio_unitario = capturar_precio("  Precio unitario ($): ")

    else:
        raise ValueError(f"Modo '{modo}' no reconocido. Elige A o B.")

    cantidad = capturar_entero("  Cantidad: ", minimo=1)
    subtotal = round(precio_unitario * cantidad, 2)

    # ── Construcción del diccionario del pedido ───────────────────
    pedido: dict = {
        "id": len(pedidos) + 1,
        "producto": nombre_producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    pedidos.append(pedido)

    print(f"\n  ✔ Pedido #{pedido['id']} registrado exitosamente.")
    print(f"    {nombre_producto} × {cantidad} = ${subtotal:.2f}")


# ─────────────────────────────────────────────────────────────────
# CONSULTA DE PEDIDOS
# ─────────────────────────────────────────────────────────────────

def consultar_pedidos(pedidos: list) -> None:
    """
    Muestra en pantalla todos los pedidos registrados en memoria.

    Args:
        pedidos (list): Lista de diccionarios con los pedidos.
    """
    imprimir_encabezado("Consultar Pedidos")

    if not pedidos:
        print("\n  ⚠ No hay pedidos registrados en memoria.")
        return

    print(
        f"\n  {'ID':<5}{'Producto':<25}{'Cant':>5}{'P.Unit':>9}{'Subtotal':>10}  {'Hora'}")
    print("  " + "─" * 58)

    for p in pedidos:
        print(
            f"  {p['id']:<5}"
            f"{p['producto']:<25}"
            f"{p['cantidad']:>5}"
            f"${p['precio_unitario']:>8.2f}"
            f"${p['subtotal']:>9.2f}"
            f"  {p['timestamp']}"
        )

    print("  " + "─" * 58)
    print(f"\n  Total de pedidos registrados: {len(pedidos)}")


# ─────────────────────────────────────────────────────────────────
# TOTAL ACUMULADO
# ─────────────────────────────────────────────────────────────────

def mostrar_total(pedidos: list) -> None:
    """
    Calcula y muestra el total acumulado de todos los pedidos.

    Utiliza una función de orden superior (sum + comprensión)
    para obtener el total de manera eficiente.

    Args:
        pedidos (list): Lista de diccionarios con los pedidos.
    """
    imprimir_encabezado("Total Acumulado")

    if not pedidos:
        print("\n  ⚠ No hay pedidos para calcular.")
        return

    total = sum(p["subtotal"] for p in pedidos)
    iva = round(total * 0.16, 2)
    total_con_iva = round(total + iva, 2)

    print(f"\n  Subtotal (sin IVA) : ${total:>10.2f}")
    print(f"  IVA (16%)          : ${iva:>10.2f}")
    print(f"  {'─' * 28}")
    print(f"  TOTAL CON IVA      : ${total_con_iva:>10.2f}")
    print(f"\n  Número de pedidos  :  {len(pedidos)}")

    # Pedido de mayor valor (uso de función built-in avanzada)
    pedido_top = max(pedidos, key=lambda p: p["subtotal"])
    print(f"  Pedido más costoso : #{pedido_top['id']} — "
          f"{pedido_top['producto']} (${pedido_top['subtotal']:.2f})")


# ─────────────────────────────────────────────────────────────────
# PERSISTENCIA — GUARDAR
# ─────────────────────────────────────────────────────────────────

def guardar_pedidos(pedidos: list, ruta: str = ARCHIVO_PEDIDOS) -> None:
    """
    Guarda la lista de pedidos en un archivo JSON.

    Incluye metadatos de la sesión (fecha, total, cantidad).
    Sobreescribe el archivo si ya existe.

    Args:
        pedidos (list): Lista de diccionarios a guardar.
        ruta    (str) : Ruta del archivo de salida.

    Raises:
        IOError: Si ocurre un error al escribir el archivo.
        PermissionError: Si no se tiene permiso de escritura.
    """
    imprimir_encabezado("Guardar Pedidos")

    if not pedidos:
        print("\n  ⚠ No hay pedidos en memoria para guardar.")
        return

    datos = {
        "cafeteria": "Café Andrómeda",
        "fecha_guardado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pedidos": len(pedidos),
        "total_acumulado": round(sum(p["subtotal"] for p in pedidos), 2),
        "pedidos": pedidos,
    }

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print(f"\n  ✔ {len(pedidos)} pedido(s) guardado(s) exitosamente.")
    print(f"  📄 Archivo: {os.path.abspath(ruta)}")


# ─────────────────────────────────────────────────────────────────
# PERSISTENCIA — LEER
# ─────────────────────────────────────────────────────────────────

def leer_pedidos(pedidos: list, ruta: str = ARCHIVO_PEDIDOS) -> None:
    """
    Carga los pedidos desde el archivo JSON hacia la lista en memoria.

    Si el archivo no existe o está vacío, informa al usuario sin
    interrumpir la ejecución del programa.

    Args:
        pedidos (list): Lista donde se cargarán los pedidos leídos.
        ruta    (str) : Ruta del archivo a leer.

    Raises:
        FileNotFoundError: Si el archivo no existe (manejado internamente).
        json.JSONDecodeError: Si el archivo tiene formato inválido.
    """
    imprimir_encabezado("Leer Pedidos desde Archivo")

    if not os.path.exists(ruta):
        print(f"\n  ⚠ El archivo '{ruta}' no existe. Guarda pedidos primero.")
        return

    if os.path.getsize(ruta) == 0:
        print(f"\n  ⚠ El archivo '{ruta}' está vacío.")
        return

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    pedidos_cargados: list = datos.get("pedidos", [])

    if not pedidos_cargados:
        print("\n  ⚠ El archivo no contiene pedidos.")
        return

    # Evitar duplicados: cargar solo IDs no presentes en memoria
    ids_actuales = {p["id"] for p in pedidos}
    nuevos = [p for p in pedidos_cargados if p["id"] not in ids_actuales]
    pedidos.extend(nuevos)

    print(f"\n  ✔ Archivo leído: {os.path.abspath(ruta)}")
    print(f"  📋 Fecha de guardado : {datos.get('fecha_guardado', 'N/D')}")
    print(f"  📦 Pedidos en archivo: {len(pedidos_cargados)}")
    print(f"  ➕ Pedidos nuevos cargados: {len(nuevos)}")
    print(f"  📊 Total en memoria ahora : {len(pedidos)}")


# ─────────────────────────────────────────────────────────────────
# BUCLE PRINCIPAL DEL SISTEMA
# ─────────────────────────────────────────────────────────────────

def ejecutar_sistema() -> None:
    """
    Bucle principal de control del sistema.

    Administra el ciclo de vida completo de la aplicación:
    muestra el menú, captura la opción, ejecuta la función
    correspondiente y maneja todas las excepciones posibles.
    """
    pedidos: list = []  # Estructura de datos principal (lista de dicts)

    print("\n  ✨ Bienvenido al Sistema de Gestión — Café Andrómeda ✨")

    # ── Ciclo principal (estructura repetitiva) ───────────────────
    while True:
        mostrar_menu_principal()

        # ── Captura y validación de opción ────────────────────────
        try:
            opcion = obtener_opcion()
        except ValueError as e:
            print(f"\n  ✘ Error de opción: {e}")
            pausar()
            continue

        # ── Despacho de opciones (estructura condicional) ─────────
        try:
            if opcion == "1":
                registrar_pedido(pedidos)

            elif opcion == "2":
                consultar_pedidos(pedidos)

            elif opcion == "3":
                mostrar_total(pedidos)

            elif opcion == "4":
                guardar_pedidos(pedidos)

            elif opcion == "5":
                leer_pedidos(pedidos)

            elif opcion == "6":
                # ── Salida segura ──────────────────────────────────
                imprimir_encabezado("Salir")
                if pedidos:
                    guardar = input(
                        f"\n  Tienes {len(pedidos)} pedido(s) en memoria.\n"
                        "  ¿Deseas guardarlos antes de salir? (s/n): "
                    ).strip().lower()
                    if guardar == "s":
                        guardar_pedidos(pedidos)

                print("\n  ¡Hasta pronto! Gracias por usar Café Andrómeda. ☕")
                print(LINEA + "\n")
                break

        # ── Manejo de errores específicos ─────────────────────────
        except ValueError as e:
            print(f"\n  ✘ Error de valor: {e}")

        except FileNotFoundError as e:
            print(f"\n  ✘ Archivo no encontrado: {e}")

        except PermissionError as e:
            print(f"\n  ✘ Sin permiso de escritura: {e}")

        except json.JSONDecodeError as e:
            print(f"\n  ✘ El archivo tiene formato inválido: {e}")

        except KeyboardInterrupt:
            print("\n\n  Interrupción detectada. Cerrando sistema...")
            break

        except Exception as e:
            # Captura genérica para errores inesperados
            print(f"\n  ✘ Error inesperado: {type(e).__name__}: {e}")

        finally:
            # El bloque finally siempre se ejecuta (incluso si hay error)
            pausar()


# ─────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ejecutar_sistema()
