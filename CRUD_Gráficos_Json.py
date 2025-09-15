import os
import json
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime, timedelta

# --- Definición de la variable para el nombre del archivo ---
archivo = "gastos.json"

# --- Categorías predefinidas para el menú ---
CATEGORIAS_PREDEFINIDAS = ['Comida', 'Transporte', 'Entretenimiento', 'Hogar', 'Salud', 'Compras', 'Otros']

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

def generar_gastos_falsos(gastos_existentes, id_contador, cantidad=50):
    """
    Genera un diccionario con una cantidad de gastos falsos y los agrega a los gastos existentes.
    """
    print(f"⚙️ Generando {cantidad} gastos de prueba...")
    
    # Listas de datos predefinidos
    descripciones = {
        'Comida': ['Almuerzo en restaurante', 'Supermercado semanal', 'Café y postre', 'Cena a domicilio'],
        'Transporte': ['Boleto de bus', 'Combustible', 'Pasaje de tren', 'Viaje en taxi'],
        'Entretenimiento': ['Entrada de cine', 'Concierto', 'Videojuego', 'Streaming mensual'],
        'Hogar': ['Factura de luz', 'Alquiler', 'Productos de limpieza', 'Reparación de grifo'],
        'Salud': ['Consulta médica', 'Medicamentos', 'Suplementos vitamínicos', 'Gimnasio'],
        'Compras': ['Ropa nueva', 'Electrónicos', 'Libro', 'Regalo de cumpleaños'],
        'Otros': ['Regalo', 'Suscripción', 'Donación', 'Servicios varios']
    }
    
    # Rango de fechas para los gastos
    fecha_hoy = datetime.now()
    rango_dias = 90
    
    for i in range(cantidad):
        categoria_random = random.choice(CATEGORIAS_PREDEFINIDAS)
        descripcion_random = random.choice(descripciones[categoria_random])
        
        monto_random = random.randint(50, 1000)
        
        # Generar una fecha aleatoria dentro del rango
        dias_atras = random.randint(0, rango_dias)
        fecha_gasto = fecha_hoy - timedelta(days=dias_atras)
        fecha_formato = fecha_gasto.strftime("%d-%m-%Y")

        gastos_existentes[str(id_contador)] = {
            'categoria': categoria_random,
            'monto': monto_random,
            'fecha': fecha_formato,
            'descripcion': descripcion_random
        }
        id_contador += 1
    
    print("✅ Datos de prueba agregados correctamente.")
    return gastos_existentes, id_contador

def cargar_gastos(nombre_archivo):
    """
    Carga los gastos desde el archivo JSON y devuelve el diccionario y el ID del próximo gasto.
    Si el archivo no existe, devuelve un diccionario vacío.
    """
    try:
        with open(nombre_archivo, 'r') as archivo:
            gastos = json.load(archivo)
        print("✅ Datos de gastos cargados desde archivo.")
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
        json.dump(gastos, archivo, indent=4, sort_keys=True) 
    print("💾 Datos de gastos guardados correctamente.")
    esperar_enter()
    return gastos

def mostrar_menu():
    """
    Muestra el menú de opciones en la consola con iconos.
    """
    print("\n----------------------------------")
    print("  💰 MENÚ DE CONTROL DE GASTOS     ")
    print("----------------------------------")
    print("1️⃣  Agregar nuevo gasto            ")
    print("2️⃣  Ver todos los gastos           ")
    print("3️⃣  Actualizar un gasto            ")
    print("4️⃣  Eliminar un gasto              ")
    print("5️⃣  Guardar gastos                 ")
    print("6️⃣  Cargar datos desde archivo JSON")
    print("7️⃣  Generar datos de prueba")
    print("--- Análisis de Gastos ---")
    print("8️⃣  Mostrar todos los gráficos")
    print("9️⃣  Mostrar un gráfico individual")
    print("0️⃣  Salir                          ")
    print("----------------------------------")

def agregar_gasto(gastos, id_contador):
    """
    Pide al usuario los datos de un nuevo gasto, lo añade al diccionario y devuelve los datos actualizados.
    Ahora incluye un menú para seleccionar la categoría.
    """
    limpiar_pantalla()
    print("--- ➕ AGREGAR NUEVO GASTO ---")
    
    # --- Nuevo menú de categorías ---
    print("\n--- 📝 SELECCIONA UNA CATEGORÍA ---")
    for i, categoria in enumerate(CATEGORIAS_PREDEFINIDAS, 1):
        print(f"{i} - {categoria}")
    
    opcion_categoria = input("➡️  Seleccione una categoría por su número: ")
    
    try:
        indice = int(opcion_categoria) - 1
        if 0 <= indice < len(CATEGORIAS_PREDEFINIDAS):
            categoria = CATEGORIAS_PREDEFINIDAS[indice]
        else:
            print("❌ Opción de categoría no válida. Se usará 'Otros'.")
            categoria = 'Otros'
    except ValueError:
        print("❌ Entrada inválida. Se usará 'Otros'.")
        categoria = 'Otros'

    # Fin del menú de categorías
    
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

    gastos[str(id_contador)] = nuevo_gasto
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
            print(f"🏷️  Categoría: {gasto_data['categoria']}")
            print(f"💸 Monto: ${gasto_data['monto']:.2f}")
            print(f"🗓️  Fecha: {gasto_data['fecha']}")
            print(f"✍️  Descripción: {gasto_data['descripcion']}")
    esperar_enter()
    return gastos

def actualizar_gasto(gastos):
    """
    Permite modificar un gasto por su ID.
    El usuario puede presionar Enter en cualquier campo para no modificarlo.
    """
    limpiar_pantalla()
    print("--- ✏️  ACTUALIZAR GASTO ---")
    if not gastos:
        print("🤷‍♂️ No hay gastos para actualizar.")
        esperar_enter()
        return gastos

    try:
        id_a_actualizar = input("🔢 Ingrese el ID del gasto a actualizar: ")
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
    print("--- 🗑️  ELIMINAR GASTO ---")
    if not gastos:
        print("🤷‍♂️ No hay gastos para eliminar.")
        esperar_enter()
        return gastos

    try:
        id_a_eliminar = input("🔢 Ingrese el ID del gasto a eliminar: ")
    except ValueError:
        print("❌ ID inválido. Ingrese un número entero.")
        esperar_enter()
        return gastos

    if id_a_eliminar in gastos:
        del gastos[id_a_eliminar]
        print("\n🗑️  Gasto eliminado con éxito.")
    else:
        print("❌ ID no encontrado.")
    
    esperar_enter()
    return gastos

def mostrar_grafico_individual(gastos):
    """
    Muestra un menú para seleccionar y ver un gráfico a la vez.
    """
    if not gastos:
        print("🤷‍♂️ No hay gastos para generar gráficos.")
        esperar_enter()
        return

    while True:
        limpiar_pantalla()
        print("\n--- 📊 SUB-MENÚ DE GRÁFICOS ---")
        print("1️⃣  Histograma: Cantidad de gastos por categoría")
        print("2️⃣  Gráfico de Barras: Monto total por categoría")
        print("3️⃣  Boxplot: Distribución de montos por categoría")
        print("4️⃣  Gráfico Circular: Proporción de gastos por categoría")
        print("5️⃣  Volver al menú principal")
        print("---------------------------------")
        
        opcion_grafico = input("➡️  Seleccione un gráfico para ver: ")

        if opcion_grafico == '1':
            ver_histograma(gastos)
        elif opcion_grafico == '2':
            ver_barras(gastos)
        elif opcion_grafico == '3':
            ver_boxplot(gastos)
        elif opcion_grafico == '4':
            ver_pie_chart(gastos)
        elif opcion_grafico == '5':
            break  # Vuelve al menú principal
        else:
            print("❌ Opción no válida. Por favor, intente de nuevo.")
            esperar_enter()

def ver_histograma(gastos):
    """
    Genera y muestra un histograma de la cantidad de gastos por categoría.
    """
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    
    plt.figure(figsize=(10, 6))
    plt.bar(gastos_por_categoria.keys(), gastos_por_categoria.values(), color='skyblue')
    plt.title('Cantidad de Gastos por Categoría', weight='bold')
    plt.xlabel('Categoría')
    plt.ylabel('Número de Gastos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def ver_barras(gastos):
    """
    Genera y muestra un gráfico de barras del monto total por categoría.
    """
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    total_por_categoria = {cat: sum(gasto['monto'] for gasto in gastos.values() if gasto['categoria'] == cat) for cat in set(categorias)}
    
    plt.figure(figsize=(10, 6))
    plt.bar(total_por_categoria.keys(), total_por_categoria.values(), color='lightgreen')
    plt.title('Monto Total por Categoría', weight='bold')
    plt.xlabel('Categoría')
    plt.ylabel('Monto Total ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def ver_boxplot(gastos):
    """
    Genera y muestra un boxplot de la distribución de montos por categoría.
    """
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    montos_por_cat = {cat: [] for cat in set(categorias)}
    for gasto in gastos.values():
        montos_por_cat[gasto['categoria']].append(gasto['monto'])
    
    data_to_plot = [montos_por_cat[cat] for cat in montos_por_cat]
    labels = list(montos_por_cat.keys())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(data_to_plot, labels=labels)
    plt.title('Distribución de Montos por Categoría (Boxplot)', weight='bold')
    plt.ylabel('Monto ($)')
    plt.xticks(rotation=45)
    plt.ylim(0, 1500)
    plt.tight_layout()
    plt.show()

def ver_pie_chart(gastos):
    """
    Genera y muestra un gráfico circular de la proporción de gastos por categoría.
    """
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    
    plt.figure(figsize=(8, 8))
    plt.pie(gastos_por_categoria.values(), labels=gastos_por_categoria.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Proporción de Gastos por Categoría', weight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def mostrar_todos_los_graficos(gastos):
    """
    Genera y muestra los 4 gráficos en una sola ventana.
    """
    if not gastos:
        print("🤷‍♂️ No hay gastos para generar gráficos.")
        esperar_enter()
        return

    categorias = [gasto['categoria'] for gasto in gastos.values()]
    montos = [gasto['monto'] for gasto in gastos.values()]
    
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    total_por_categoria = {cat: sum(gasto['monto'] for gasto in gastos.values() if gasto['categoria'] == cat) for cat in set(categorias)}
    
    # Crear la figura y los subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('📊 Análisis de Gastos', fontsize=20, weight='bold')
    
    # Ajustar el espacio entre subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.8)  # Aumenta hspace (espacio vertical)
    
    # Histograma de Cantidad de Gastos por Categoría
    axs[0, 0].bar(gastos_por_categoria.keys(), gastos_por_categoria.values(), color='skyblue')
    axs[0, 0].set_title('Cantidad de Gastos por Categoría', weight='bold')
    axs[0, 0].set_xlabel('Categoría')
    axs[0, 0].set_ylabel('Número de Gastos')
    axs[0, 0].tick_params(axis='x', rotation=45)
    
    # Gráfico de Barras de Monto Total por Categoría
    axs[0, 1].bar(total_por_categoria.keys(), total_por_categoria.values(), color='lightgreen')
    axs[0, 1].set_title('Monto Total por Categoría', weight='bold')
    axs[0, 1].set_xlabel('Categoría')
    axs[0, 1].set_ylabel('Monto Total ($)')
    axs[0, 1].tick_params(axis='x', rotation=45)
    
    # Boxplot de la Distribución de Gastos
    montos_por_cat = {cat: [] for cat in set(categorias)}
    for gasto in gastos.values():
        montos_por_cat[gasto['categoria']].append(gasto['monto'])
    
    data_to_plot = [montos_por_cat[cat] for cat in montos_por_cat]
    labels = list(montos_por_cat.keys())
    
    axs[1, 0].boxplot(data_to_plot, labels=labels)
    axs[1, 0].set_title('Distribución de Montos por Categoría (Boxplot)', weight='bold')
    axs[1, 0].set_ylabel('Monto ($)')
    axs[1, 0].tick_params(axis='x', rotation=45)
    axs[1, 0].set_ylim(0, 1500)
    
    # Gráfico Circular (Pie Chart) de Cantidad de Gastos
    axs[1, 1].pie(gastos_por_categoria.values(), labels=gastos_por_categoria.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    axs[1, 1].set_title('Proporción de Gastos por Categoría', weight='bold')
    axs[1, 1].axis('equal')
    
    # Mostrar la figura con los subplots
    plt.show()


# --- Bucle Principal del Programa ---
gastos, id_contador = cargar_gastos(archivo)

while True:
    limpiar_pantalla()
    mostrar_menu()
    
    opcion = input("➡️  Seleccione una opción: ")
    
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
        gastos, id_contador = generar_gastos_falsos(gastos, id_contador)
        esperar_enter()
    elif opcion == '8':
        mostrar_todos_los_graficos(gastos)
    elif opcion == '9':
        mostrar_grafico_individual(gastos)
    elif opcion == '0':
        print("👋 Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("❌ Opción no válida. Por favor, intente de nuevo.")
        esperar_enter()