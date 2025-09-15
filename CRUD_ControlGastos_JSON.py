import os  # Módulo para interactuar con el sistema operativo (limpiar pantalla).
import json  # Módulo para trabajar con archivos en formato JSON.

# --- Definición de la variable para el nombre del archivo ---
archivo = "gastos.json"

def limpiar_pantalla():
    """
    Función para limpiar la pantalla de la consola.
    'cls' es para sistemas Windows, 'clear' es para Linux y macOS.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar_enter():
    """
    Función que pide al usuario presionar la tecla Enter para continuar.
    """
    input("\nPresiona Enter para continuar...")

def cargar_gastos(nombre_archivo):
    """
    Carga los gastos desde el archivo JSON y devuelve el diccionario y el ID del próximo gasto.
    Si el archivo no existe, devuelve un diccionario vacío.
    """
    try:
        with open(nombre_archivo, 'r') as archivo:
            gastos = json.load(archivo)
        print("✅ Datos de gastos cargados correctamente.")
        if gastos:
            ultimo_id = max(int(id) for id in gastos.keys())
            id_contador = ultimo_id + 1
        else:
            id_contador = 1
    except FileNotFoundError:
        print("⚠️ El archivo de datos no existe. Se iniciará con un diccionario de gastos vacío.")
        gastos = {}
        id_contador = 1
    
    esperar_enter()
    return gastos, id_contador

def guardar_gastos(gastos, nombre_archivo):
    """
    Guarda el diccionario de gastos en el archivo JSON.
    """
    with open(nombre_archivo, 'w') as archivo:
        json.dump(gastos, archivo, indent=4)
    print("💾 Datos de gastos guardados correctamente.")
    esperar_enter()
    return gastos

def mostrar_menu():
    """
    Muestra el menú de opciones en la consola con iconos.
    """
    print("\n---------------------------------")
    print("  💰 MENÚ DE CONTROL DE GASTOS    ")
    print("---------------------------------")
    print("1️⃣  Agregar nuevo gasto           ")
    print("2️⃣  Ver todos los gastos          ")
    print("3️⃣  Actualizar un gasto           ")
    print("4️⃣  Eliminar un gasto             ")
    print("5️⃣  Guardar gastos                ")
    print("6️⃣  Cargar datos desde archivo JSON")
    print("7️⃣  Salir                         ")
    print("---------------------------------")

def agregar_gasto(gastos, id_contador):
    """
    Pide al usuario los datos de un nuevo gasto, lo añade al diccionario y devuelve los datos actualizados.
    """
    limpiar_pantalla()
    print("--- ➕ AGREGAR NUEVO GASTO ---")
    
    categoria = input("📝 Ingrese la categoría (ej: Comida): ")
    try:
        monto = float(input("💲 Ingrese el monto (ej: 15.50): "))
    except ValueError:
        print("❌ Monto inválido. Ingrese un número.")
        esperar_enter()
        return gastos, id_contador

    fecha = input("📅 Ingrese la fecha (ej: 15-09-2025): ")
    descripcion = input("📄 Ingrese una breve descripción: ")

    nuevo_gasto = {
        'categoria': categoria,
        'monto': monto,
        'fecha': fecha,
        'descripcion': descripcion
    }

    gastos[id_contador] = nuevo_gasto
    id_contador += 1
    print("\n✅ Gasto agregado con éxito.")
    esperar_enter()
    return gastos, id_contador

def ver_gastos(gastos):
    """
    Muestra todos los gastos del diccionario.
    """
    limpiar_pantalla()
    print("--- 📋 LISTA DE GASTOS ---")
    if not gastos:
        print("🤷‍♂️ No hay gastos registrados.")
    else:
        for gasto_id, gasto_data in gastos.items():
            print(f"\n#️⃣ ID: {gasto_id}")
            print(f"🏷️  Categoría: {gasto_data['categoria']}")
            print(f"💸 Monto: ${gasto_data['monto']:.2f}")
            print(f"🗓️  Fecha: {gasto_data['fecha']}")
            print(f"✍️  Descripción: {gasto_data['descripcion']}")
    esperar_enter()
    return gastos

def actualizar_gasto(gastos):
    """
    Permite modificar un gasto por su ID.
    El usuario puede presionar Enter en cualquier campo para no modificarlo.
    """
    limpiar_pantalla()
    print("--- ✏️  ACTUALIZAR GASTO ---")
    if not gastos:
        print("🤷‍♂️ No hay gastos para actualizar.")
        esperar_enter()
        return gastos

    try:
        id_a_actualizar = int(input("🔢 Ingrese el ID del gasto a actualizar: "))
    except ValueError:
        print("❌ ID inválido. Ingrese un número entero.")
        esperar_enter()
        return gastos

    if id_a_actualizar in gastos:
        gasto_data = gastos[id_a_actualizar]
        print("\n✅ Se encontró el gasto. Ingrese los nuevos datos (presione Enter para no modificar):")
        
        nueva_categoria = input(f"📝 Nueva categoría ({gasto_data['categoria']}): ")
        if nueva_categoria:
            gasto_data['categoria'] = nueva_categoria

        while True:
            nuevo_monto_str = input(f"💲 Nuevo monto ({gasto_data['monto']:.2f}): ")
            if not nuevo_monto_str:
                break
            try:
                gasto_data['monto'] = float(nuevo_monto_str)
                break
            except ValueError:
                print("❌ Monto inválido. Ingrese un número o presione Enter.")

        nueva_fecha = input(f"📅 Nueva fecha ({gasto_data['fecha']}): ")
        if nueva_fecha:
            gasto_data['fecha'] = nueva_fecha

        nueva_descripcion = input(f"📄 Nueva descripción ({gasto_data['descripcion']}): ")
        if nueva_descripcion:
            gasto_data['descripcion'] = nueva_descripcion
        
        print("\n✅ Gasto actualizado con éxito.")
    else:
        print("❌ ID no encontrado.")
    
    esperar_enter()
    return gastos

def eliminar_gasto(gastos):
    """
    Elimina un gasto del diccionario por su ID.
    """
    limpiar_pantalla()
    print("--- 🗑️  ELIMINAR GASTO ---")
    if not gastos:
        print("🤷‍♂️ No hay gastos para eliminar.")
        esperar_enter()
        return gastos

    try:
        id_a_eliminar = int(input("🔢 Ingrese el ID del gasto a eliminar: "))
    except ValueError:
        print("❌ ID inválido. Ingrese un número entero.")
        esperar_enter()
        return gastos

    if id_a_eliminar in gastos:
        del gastos[id_a_eliminar]
        print("\n🗑️  Gasto eliminado con éxito.")
    else:
        print("❌ ID no encontrado.")
    
    esperar_enter()
    return gastos

# --- Bucle Principal del Programa ---
gastos, id_contador = cargar_gastos(archivo)

while True:
    limpiar_pantalla()
    mostrar_menu()
    
    opcion = input("➡️  Seleccione una opción: ")
    
    if opcion == '1':
        gastos, id_contador = agregar_gasto(gastos, id_contador)
    elif opcion == '2':
        gastos = ver_gastos(gastos)
    elif opcion == '3':
        gastos = actualizar_gasto(gastos)
    elif opcion == '4':
        gastos = eliminar_gasto(gastos)
    elif opcion == '5':
        gastos = guardar_gastos(gastos, archivo)
    elif opcion == '6':
        print("🔃 Cargando los datos desde el archivo...")
        gastos, id_contador = cargar_gastos(archivo)
    elif opcion == '7':
        print("👋 Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("❌ Opción no válida. Por favor, intente de nuevo.")
        esperar_enter()