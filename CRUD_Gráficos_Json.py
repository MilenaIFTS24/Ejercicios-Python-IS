import os
# Importa el módulo 'os', que proporciona una forma de usar funcionalidades
# dependientes del sistema operativo, como limpiar la consola.

import json
# Importa el módulo 'json' para codificar y decodificar datos en formato JSON,
# lo que permite guardar y cargar la información de gastos en un archivo.

import matplotlib.pyplot as plt
# Importa la biblioteca 'matplotlib.pyplot' con el alias 'plt', que se utiliza
# para crear visualizaciones estáticas e interactivas en Python, como gráficos.

import numpy as np
# Importa la biblioteca 'numpy' con el alias 'np', fundamental para la
# computación científica en Python. Se usa para operaciones numéricas eficientes.

import random
# Importa el módulo 'random' para generar números y elementos aleatorios,
# lo cual es útil para crear datos de prueba falsos.

from datetime import datetime, timedelta
# Importa las clases 'datetime' y 'timedelta' del módulo 'datetime', que
# permiten manipular fechas y horas, como calcular una fecha en el pasado.

# --- Definición de la variable para el nombre del archivo ---
archivo = "gastos.json"
# Define una variable de cadena que contiene el nombre del archivo donde se
# almacenarán los datos de los gastos.

# --- Categorías predefinidas para el menú ---
CATEGORIAS_PREDEFINIDAS = ['Comida', 'Transporte', 'Entretenimiento', 'Hogar', 'Salud', 'Compras', 'Otros']
# Define una lista de cadenas con las categorías de gastos disponibles,
# utilizada para la selección en el menú.

def limpiar_pantalla():
    """
    Función para limpiar la pantalla de la consola.
    'cls' es para sistemas Windows, 'clear' es para Linux y macOS.
    """
    # Define la función para limpiar la consola.
    os.system('cls' if os.name == 'nt' else 'clear')
    # Utiliza la función `os.system()` para ejecutar un comando del sistema.
    # El comando es 'cls' si el sistema operativo es Windows (os.name == 'nt'),
    # de lo contrario, es 'clear' para sistemas Unix como Linux o macOS.

def esperar_enter():
    """
    Función que pide al usuario presionar la tecla Enter para continuar.
    """
    # Define la función para pausar la ejecución del programa.
    input("\nPresiona Enter para continuar...")
    # La función `input()` muestra un mensaje y espera a que el usuario
    # presione Enter, deteniendo el flujo del programa.

def generar_gastos_falsos(gastos_existentes, id_contador, cantidad=100):
    """
    Genera un diccionario con una cantidad de gastos falsos y los agrega a los gastos existentes.
    """
    # Define la función para generar datos de prueba.
    print(f"⚙️ Generando {cantidad} gastos de prueba...")
    # Imprime un mensaje indicando el inicio de la generación de datos.
    
    # Listas de datos predefinidos
    # Comentario para la sección de datos predefinidos.
    descripciones = {
    # Crea un diccionario de listas de descripciones, una por cada categoría.
        'Comida': ['Almuerzo en restaurante', 'Supermercado semanal', 'Café y postre', 'Cena a domicilio'],
        'Transporte': ['Boleto de bus', 'Combustible', 'Pasaje de tren', 'Viaje en taxi'],
        'Entretenimiento': ['Entrada de cine', 'Concierto', 'Videojuego', 'Streaming mensual'],
        'Hogar': ['Factura de luz', 'Alquiler', 'Productos de limpieza', 'Reparación de grifo'],
        'Salud': ['Consulta médica', 'Medicamentos', 'Suplementos vitamínicos', 'Gimnasio'],
        'Compras': ['Ropa nueva', 'Electrónicos', 'Libro', 'Regalo de cumpleaños'],
        'Otros': ['Regalo', 'Suscripción', 'Donación', 'Servicios varios']
    }
    
    # Rango de fechas para los gastos
    # Comentario para la sección de fechas.
    fecha_hoy = datetime.now()
    # Obtiene la fecha y hora actuales.
    rango_dias = 90
    # Define la cantidad de días hacia atrás a partir de hoy para generar fechas.
    
    for i in range(cantidad):
    # Inicia un bucle que se ejecuta 'cantidad' de veces para crear cada gasto.
        categoria_random = random.choice(CATEGORIAS_PREDEFINIDAS)
        # Elige una categoría al azar de la lista predefinida.
        descripcion_random = random.choice(descripciones[categoria_random])
        # Elige una descripción al azar de la lista correspondiente a la categoría elegida.
        
        monto_random = random.randint(50, 1000)
        # Genera un número entero aleatorio para el monto entre 50 y 1000.
        
        # Generar una fecha aleatoria dentro del rango
        # Comentario.
        dias_atras = random.randint(0, rango_dias)
        # Genera un número aleatorio de días para restar a la fecha actual.
        fecha_gasto = fecha_hoy - timedelta(days=dias_atras)
        # Calcula la fecha del gasto restando los días aleatorios a la fecha actual.
        fecha_formato = fecha_gasto.strftime("%d-%m-%Y")
        # Formatea el objeto de fecha a una cadena con el formato "día-mes-año".

        gastos_existentes[str(id_contador)] = {
        # Agrega un nuevo gasto al diccionario `gastos_existentes` usando el contador
        # como clave, convertido a cadena.
            'categoria': categoria_random,
        # Asigna la categoría aleatoria.
            'monto': monto_random,
        # Asigna el monto aleatorio.
            'fecha': fecha_formato,
        # Asigna la fecha formateada.
            'descripcion': descripcion_random
        # Asigna la descripción aleatoria.
        }
        id_contador += 1
        # Incrementa el contador de ID en 1 para el siguiente gasto.
    
    print("✅ Datos de prueba agregados correctamente.")
    # Imprime un mensaje de éxito.
    return gastos_existentes, id_contador
    # Devuelve el diccionario de gastos actualizado y el nuevo contador de ID.

def cargar_gastos(nombre_archivo):
    """
    Carga los gastos desde el archivo JSON y devuelve el diccionario y el ID del próximo gasto.
    Si el archivo no existe, devuelve un diccionario vacío.
    """
    # Define la función para cargar datos de un archivo.
    try:
    # Inicia un bloque `try` para manejar el caso en que el archivo no exista.
        with open(nombre_archivo, 'r') as archivo:
        # Abre el archivo en modo de lectura ('r'). `with` asegura que el archivo se cierre.
            gastos = json.load(archivo)
        # Carga los datos del archivo JSON a un diccionario de Python.
        print("✅ Datos de gastos cargados desde archivo.")
        # Imprime un mensaje de éxito.
        if gastos:
        # Comprueba si el diccionario `gastos` no está vacío.
            ultimo_id = max(int(id) for id in gastos.keys())
        # Encuentra el ID numérico más alto entre las claves del diccionario.
            id_contador = ultimo_id + 1
        # Establece el contador para el siguiente ID disponible.
        else:
        # Si el diccionario está vacío.
            id_contador = 1
        # Inicia el contador en 1.
    except FileNotFoundError:
    # Captura la excepción `FileNotFoundError` si el archivo no existe.
        print("⚠️ El archivo de datos no existe. Se iniciará con un diccionario de gastos vacío.")
        # Muestra un mensaje de advertencia.
        gastos = {}
        # Inicializa el diccionario de gastos como vacío.
        id_contador = 1
        # Inicia el contador en 1.
    
    esperar_enter()
    # Llama a la función para pausar y esperar la interacción del usuario.
    return gastos, id_contador
    # Devuelve el diccionario y el contador de ID.

def guardar_gastos(gastos, nombre_archivo):
    """
    Guarda el diccionario de gastos en el archivo JSON.
    """
    # Define la función para guardar datos en un archivo.
    with open(nombre_archivo, 'w') as archivo:
    # Abre el archivo en modo de escritura ('w'), lo que sobrescribe su contenido.
        json.dump(gastos, archivo, indent=4, sort_keys=True) 
    # Guarda el diccionario `gastos` como JSON en el archivo. `indent` formatea
    # el archivo para que sea legible, y `sort_keys` lo ordena por clave.
    print("💾 Datos de gastos guardados correctamente.")
    # Imprime un mensaje de éxito.
    esperar_enter()
    # Pausa la ejecución.
    return gastos
    # Devuelve el diccionario de gastos.

def mostrar_menu():
    """
    Muestra el menú de opciones en la consola con iconos.
    """
    # Define la función para mostrar las opciones del menú.
    print("\n----------------------------------")
    # Imprime una línea separadora.
    print("  💰 MENÚ DE CONTROL DE GASTOS     ")
    # Imprime el título del menú.
    print("----------------------------------")
    # Imprime una línea separadora.
    print("1️⃣  Agregar nuevo gasto            ")
    # Imprime la opción 1.
    print("2️⃣  Ver todos los gastos           ")
    # Imprime la opción 2.
    print("3️⃣  Actualizar un gasto            ")
    # Imprime la opción 3.
    print("4️⃣  Eliminar un gasto              ")
    # Imprime la opción 4.
    print("5️⃣  Guardar gastos                 ")
    # Imprime la opción 5.
    print("6️⃣  Cargar datos desde archivo JSON")
    # Imprime la opción 6.
    print("7️⃣  Generar datos de prueba")
    # Imprime la opción 7.
    print("--- Análisis de Gastos ---")
    # Imprime un separador visual para la sección de análisis.
    print("8️⃣  Mostrar todos los gráficos")
    # Imprime la opción 8.
    print("9️⃣  Mostrar un gráfico individual")
    # Imprime la opción 9.
    print("0️⃣  Salir                          ")
    # Imprime la opción 0.
    print("----------------------------------")
    # Imprime una línea separadora.

def agregar_gasto(gastos, id_contador):
    """
    Pide al usuario los datos de un nuevo gasto, lo añade al diccionario y devuelve los datos actualizados.
    Ahora incluye un menú para seleccionar la categoría.
    """
    # Define la función para agregar un gasto.
    limpiar_pantalla()
    # Limpia la consola.
    print("--- ➕ AGREGAR NUEVO GASTO ---")
    # Imprime el título de la sección.
    
    # --- Nuevo menú de categorías ---
    # Comentario.
    print("\n--- 📝 SELECCIONA UNA CATEGORÍA ---")
    # Imprime el título para la selección de categoría.
    for i, categoria in enumerate(CATEGORIAS_PREDEFINIDAS, 1):
    # Itera sobre la lista de categorías, asignando un número secuencial a cada una.
        print(f"{i} - {categoria}")
    # Imprime el número y el nombre de cada categoría.
    
    opcion_categoria = input("➡️  Seleccione una categoría por su número: ")
    # Pide al usuario que elija una categoría por su número.
    
    try:
    # Inicia un bloque `try` para manejar errores de conversión.
        indice = int(opcion_categoria) - 1
    # Convierte la entrada a un entero y resta 1 para obtener el índice de la lista.
        if 0 <= indice < len(CATEGORIAS_PREDEFINIDAS):
        # Verifica que el índice esté dentro del rango válido de la lista.
            categoria = CATEGORIAS_PREDEFINIDAS[indice]
        # Asigna la categoría seleccionada.
        else:
        # Si el índice no es válido.
            print("❌ Opción de categoría no válida. Se usará 'Otros'.")
        # Imprime un mensaje de error.
            categoria = 'Otros'
        # Asigna la categoría por defecto 'Otros'.
    except ValueError:
    # Captura el error si la entrada del usuario no es un número.
        print("❌ Entrada inválida. Se usará 'Otros'.")
    # Imprime un mensaje de error.
        categoria = 'Otros'
    # Asigna la categoría por defecto 'Otros'.

    # Fin del menú de categorías
    # Comentario.
    
    try:
    # Inicia un bloque `try` para manejar errores en la entrada del monto.
        monto = float(input("💲 Ingrese el monto (ej: 15.50): "))
    # Pide el monto y lo convierte a un número de punto flotante.
    except ValueError:
    # Captura el error si la entrada no es un número.
        print("❌ Monto inválido. Ingrese un número.")
    # Imprime un mensaje de error.
        esperar_enter()
    # Pausa la ejecución.
        return gastos, id_contador
    # Devuelve el estado sin cambios.

    fecha = input("📅 Ingrese la fecha (ej: 15-09-2025): ")
    # Pide la fecha del gasto como una cadena de texto.
    descripcion = input("📄 Ingrese una breve descripción: ")
    # Pide una breve descripción.

    nuevo_gasto = {
    # Crea un diccionario para almacenar los datos del nuevo gasto.
        'categoria': categoria,
        'monto': monto,
        'fecha': fecha,
        'descripcion': descripcion
    }

    gastos[str(id_contador)] = nuevo_gasto
    # Agrega el nuevo gasto al diccionario `gastos` con el ID actual como clave.
    id_contador += 1
    # Incrementa el contador para el próximo gasto.
    print("\n✅ Gasto agregado con éxito.")
    # Imprime un mensaje de éxito.
    esperar_enter()
    # Pausa la ejecución.
    return gastos, id_contador
    # Devuelve el diccionario de gastos actualizado y el contador.

def ver_gastos(gastos):
    """
    Muestra todos los gastos del diccionario.
    """
    # Define la función para ver los gastos.
    limpiar_pantalla()
    # Limpia la consola.
    print("--- 📋 LISTA DE GASTOS ---")
    # Imprime el título de la lista.
    if not gastos:
    # Verifica si el diccionario de gastos está vacío.
        print("🤷‍♂️ No hay gastos registrados.")
    # Muestra un mensaje si no hay gastos.
    else:
    # Si hay gastos, ejecuta el siguiente bloque.
        for gasto_id, gasto_data in gastos.items():
        # Itera sobre cada par de clave-valor (ID y datos) en el diccionario.
            print(f"\n#️⃣ ID: {gasto_id}")
            # Imprime el ID del gasto.
            print(f"🏷️  Categoría: {gasto_data['categoria']}")
            # Imprime la categoría.
            print(f"💸 Monto: ${gasto_data['monto']:.2f}")
            # Imprime el monto formateado con dos decimales.
            print(f"🗓️  Fecha: {gasto_data['fecha']}")
            # Imprime la fecha.
            print(f"✍️  Descripción: {gasto_data['descripcion']}")
            # Imprime la descripción.
    esperar_enter()
    # Pausa la ejecución.
    return gastos
    # Devuelve el diccionario de gastos.

def actualizar_gasto(gastos):
    """
    Permite modificar un gasto por su ID.
    El usuario puede presionar Enter en cualquier campo para no modificarlo.
    """
    # Define la función para actualizar un gasto.
    limpiar_pantalla()
    # Limpia la consola.
    print("--- ✏️  ACTUALIZAR GASTO ---")
    # Imprime el título.
    if not gastos:
    # Verifica si el diccionario de gastos está vacío.
        print("🤷‍♂️ No hay gastos para actualizar.")
    # Muestra un mensaje si no hay gastos.
        esperar_enter()
    # Pausa la ejecución.
        return gastos
    # Devuelve el estado sin cambios.

    try:
    # Inicia un bloque `try`.
        id_a_actualizar = input("🔢 Ingrese el ID del gasto a actualizar: ")
    # Pide al usuario el ID del gasto a actualizar.
    except ValueError:
    # Captura el error si el ID no es un entero.
        print("❌ ID inválido. Ingrese un número entero.")
    # Muestra un mensaje de error.
        esperar_enter()
    # Pausa la ejecución.
        return gastos
    # Devuelve el estado sin cambios.

    if id_a_actualizar in gastos:
    # Verifica si el ID ingresado existe como clave en el diccionario.
        gasto_data = gastos[id_a_actualizar]
    # Asigna los datos del gasto a la variable `gasto_data`.
        print("\n✅ Se encontró el gasto. Ingrese los nuevos datos (presione Enter para no modificar):")
    # Imprime un mensaje de éxito.
        
        nueva_categoria = input(f"📝 Nueva categoría ({gasto_data['categoria']}): ")
    # Pide la nueva categoría, mostrando la actual entre paréntesis.
        if nueva_categoria:
        # Si el usuario ingresa un valor (no una cadena vacía).
            gasto_data['categoria'] = nueva_categoria
        # Actualiza la categoría.

        while True:
        # Inicia un bucle para validar la entrada del monto.
            nuevo_monto_str = input(f"💲 Nuevo monto ({gasto_data['monto']:.2f}): ")
        # Pide el nuevo monto, mostrando el actual formateado.
            if not nuevo_monto_str:
            # Si la entrada es una cadena vacía (el usuario presiona Enter).
                break
            # Sale del bucle.
            try:
            # Inicia un bloque `try` para la conversión.
                gasto_data['monto'] = float(nuevo_monto_str)
            # Convierte y actualiza el monto.
                break
            # Sale del buucle si la conversión es exitosa.
            except ValueError:
            # Captura el error si la entrada no es un número.
                print("❌ Monto inválido. Ingrese un número o presione Enter.")
            # Muestra un mensaje de error.

        nueva_fecha = input(f"📅 Nueva fecha ({gasto_data['fecha']}): ")
    # Pide la nueva fecha.
        if nueva_fecha:
        # Si la entrada no es vacía.
            gasto_data['fecha'] = nueva_fecha
        # Actualiza la fecha.

        nueva_descripcion = input(f"📄 Nueva descripción ({gasto_data['descripcion']}): ")
    # Pide la nueva descripción.
        if nueva_descripcion:
        # Si la entrada no es vacía.
            gasto_data['descripcion'] = nueva_descripcion
        # Actualiza la descripción.
        
        print("\n✅ Gasto actualizado con éxito.")
    # Imprime un mensaje de éxito.
    else:
    # Si el ID no se encontró.
        print("❌ ID no encontrado.")
    # Muestra un mensaje de error.
    
    esperar_enter()
    # Pausa la ejecución.
    return gastos
    # Devuelve el diccionario de gastos.

def eliminar_gasto(gastos):
    """
    Elimina un gasto del diccionario por su ID, solicitando confirmación al usuario.
    """
    # Define la función para eliminar un gasto con confirmación.
    limpiar_pantalla()
    # Limpia la consola.
    print("--- 🗑️  ELIMINAR GASTO ---")
    # Imprime el título.
    if not gastos:
    # Verifica si el diccionario de gastos está vacío.
        print("🤷‍♂️ No hay gastos para eliminar.")
    # Muestra un mensaje de advertencia.
        esperar_enter()
    # Pausa la ejecución.
        return gastos
    # Devuelve el estado sin cambios.

    try:
    # Inicia un bloque `try`.
        id_a_eliminar = input("🔢 Ingrese el ID del gasto a eliminar: ")
    # Pide el ID del gasto a eliminar.
    except ValueError:
    # Captura el error si la entrada no es un entero.
        print("❌ ID inválido. Ingrese un número entero.")
    # Muestra un mensaje de error.
        esperar_enter()
    # Pausa la ejecución.
        return gastos
    # Devuelve el estado sin cambios.

    if id_a_eliminar in gastos:
    # Verifica si el ID existe en el diccionario.
        print(f"\n❓ ¿Estás seguro de que deseas eliminar el gasto con ID {id_a_eliminar}?")
    # Muestra el mensaje de confirmación, incluyendo el ID del gasto.
        confirmacion = input("Escribe 'si' para confirmar, o cualquier otra cosa para cancelar: ").lower()
    # Pide la confirmación al usuario y convierte la respuesta a minúsculas.
        if confirmacion == 'si':
        # Comprueba si la respuesta del usuario es 'si'.
            del gastos[id_a_eliminar]
        # Elimina el gasto del diccionario usando el ID como clave.
            print("\n🗑️  Gasto eliminado con éxito.")
        # Muestra un mensaje de éxito.
        else:
        # Si la respuesta no es 'si'.
            print("\n✅ Eliminación cancelada.")
        # Muestra un mensaje de cancelación.
    else:
    # Si el ID no se encontró en el diccionario.
        print("❌ ID no encontrado.")
    # Muestra un mensaje de error.
    
    esperar_enter()
    # Pausa la ejecución.
    return gastos
    # Devuelve el diccionario de gastos actualizado.

def mostrar_grafico_individual(gastos):
    """
    Muestra un menú para seleccionar y ver un gráfico a la vez.
    """
    # Define la función para mostrar un submenú de gráficos.
    if not gastos:
    # Verifica si no hay gastos para graficar.
        print("🤷‍♂️ No hay gastos para generar gráficos.")
    # Muestra un mensaje de advertencia.
        esperar_enter()
    # Pausa la ejecución.
        return
    # Sale de la función.

    while True:
    # Inicia un bucle infinito para el submenú.
        limpiar_pantalla()
    # Limpia la consola.
        print("\n--- 📊 SUB-MENÚ DE GRÁFICOS ---")
    # Imprime el título del submenú.
        print("1️⃣  Histograma: Cantidad de gastos por categoría")
        # Opción 1.
        print("2️⃣  Gráfico de Barras: Monto total por categoría")
        # Opción 2.
        print("3️⃣  Boxplot: Distribución de montos por categoría")
        # Opción 3.
        print("4️⃣  Gráfico Circular: Proporción de gastos por categoría")
        # Opción 4.
        print("5️⃣  Volver al menú principal")
        # Opción 5.
        print("---------------------------------")
        # Línea separadora.
        
        opcion_grafico = input("➡️  Seleccione un gráfico para ver: ")
        # Pide al usuario que seleccione una opción.

        if opcion_grafico == '1':
        # Si la opción es '1'.
            ver_histograma(gastos)
        # Llama a la función para el histograma.
        elif opcion_grafico == '2':
        # Si la opción es '2'.
            ver_barras(gastos)
        # Llama a la función para el gráfico de barras.
        elif opcion_grafico == '3':
        # Si la opción es '3'.
            ver_boxplot(gastos)
        # Llama a la función para el boxplot.
        elif opcion_grafico == '4':
        # Si la opción es '4'.
            ver_pie_chart(gastos)
        # Llama a la función para el gráfico circular.
        elif opcion_grafico == '5':
        # Si la opción es '5'.
            break
        # Sale del bucle `while True`, regresando al menú principal.
        else:
        # Para cualquier otra entrada.
            print("❌ Opción no válida. Por favor, intente de nuevo.")
        # Muestra un mensaje de error.
            esperar_enter()
        # Pausa la ejecución.

def ver_histograma(gastos):
    """
    Genera y muestra un histograma de la cantidad de gastos por categoría.
    """
    # Define la función para generar un histograma.
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    # Crea una lista de todas las categorías de los gastos.
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    # Crea un diccionario con el conteo de cada categoría.
    
    plt.figure(figsize=(10, 6))
    # Crea una nueva figura de Matplotlib con un tamaño específico.
    plt.bar(gastos_por_categoria.keys(), gastos_por_categoria.values(), color='skyblue')
    # Dibuja un gráfico de barras.
    plt.title('Cantidad de Gastos por Categoría', weight='bold')
    # Establece el título del gráfico.
    plt.xlabel('Categoría')
    # Establece la etiqueta del eje x.
    plt.ylabel('Número de Gastos')
    # Establece la etiqueta del eje y.
    plt.xticks(rotation=45)
    # Rota las etiquetas del eje x 45 grados para mejorar la legibilidad.
    plt.tight_layout()
    # Ajusta automáticamente el diseño de la figura para que no se superpongan elementos.
    plt.show()
    # Muestra el gráfico en una ventana.

def ver_barras(gastos):
    """
    Genera y muestra un gráfico de barras del monto total por categoría.
    """
    # Define la función para generar un gráfico de barras.
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    # Crea una lista de categorías.
    total_por_categoria = {cat: sum(gasto['monto'] for gasto in gastos.values() if gasto['categoria'] == cat) for cat in set(categorias)}
    # Calcula la suma total de los montos para cada categoría.
    
    plt.figure(figsize=(10, 6))
    # Crea una nueva figura.
    plt.bar(total_por_categoria.keys(), total_por_categoria.values(), color='lightgreen')
    # Dibuja un gráfico de barras.
    plt.title('Monto Total por Categoría', weight='bold')
    # Establece el título.
    plt.xlabel('Categoría')
    # Establece la etiqueta del eje x.
    plt.ylabel('Monto Total ($)')
    # Establece la etiqueta del eje y.
    plt.xticks(rotation=45)
    # Rota las etiquetas.
    plt.tight_layout()
    # Ajusta el diseño.
    plt.show()
    # Muestra el gráfico.

def ver_boxplot(gastos):
    """
    Genera y muestra un boxplot de la distribución de montos por categoría.
    """
    # Define la función para generar un boxplot.
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    # Crea una lista de categorías.
    montos_por_cat = {cat: [] for cat in set(categorias)}
    # Inicializa un diccionario con listas vacías para cada categoría.
    for gasto in gastos.values():
    # Itera sobre los datos de los gastos.
        montos_por_cat[gasto['categoria']].append(gasto['monto'])
    # Agrega el monto a la lista correspondiente a su categoría.
    
    data_to_plot = [montos_por_cat[cat] for cat in montos_por_cat]
    # Crea una lista de listas de montos, organizada por categoría.
    labels = list(montos_por_cat.keys())
    # Crea una lista de etiquetas de categorías.
    
    plt.figure(figsize=(10, 6))
    # Crea una nueva figura.
    plt.boxplot(data_to_plot, labels=labels)
    # Dibuja el boxplot.
    plt.title('Distribución de Montos por Categoría (Boxplot)', weight='bold')
    # Establece el título.
    plt.ylabel('Monto ($)')
    # Establece la etiqueta del eje y.
    plt.xticks(rotation=45)
    # Rota las etiquetas.
    plt.ylim(0, 1500)
    # Establece los límites del eje y.
    plt.tight_layout()
    # Ajusta el diseño.
    plt.show()
    # Muestra el gráfico.

def ver_pie_chart(gastos):
    """
    Genera y muestra un gráfico circular de la proporción de gastos por categoría.
    """
    # Define la función para generar un gráfico circular.
    categorias = [gasto['categoria'] for gasto in gastos.values()]
    # Crea una lista de categorías.
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    # Cuenta la cantidad de gastos por categoría.
    
    plt.figure(figsize=(8, 8))
    # Crea una figura cuadrada.
    plt.pie(gastos_por_categoria.values(), labels=gastos_por_categoria.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    # Dibuja el gráfico circular. `autopct` formatea los porcentajes, `startangle`
    # rota el gráfico, y `colors` aplica una paleta de colores.
    plt.title('Proporción de Gastos por Categoría', weight='bold')
    # Establece el título.
    plt.axis('equal')
    # Asegura que el gráfico circular sea un círculo perfecto.
    plt.tight_layout()
    # Ajusta el diseño.
    plt.show()
    # Muestra el gráfico.

def mostrar_todos_los_graficos(gastos):
    """
    Genera y muestra los 4 gráficos en una sola ventana.
    """
    # Define la función para mostrar varios gráficos a la vez.
    if not gastos:
    # Verifica si no hay gastos.
        print("🤷‍♂️ No hay gastos para generar gráficos.")
    # Muestra un mensaje de advertencia.
        esperar_enter()
    # Pausa la ejecución.
        return
    # Sale de la función.

    categorias = [gasto['categoria'] for gasto in gastos.values()]
    # Crea una lista de categorías.
    montos = [gasto['monto'] for gasto in gastos.values()]
    # Crea una lista de montos.
    
    gastos_por_categoria = {cat: categorias.count(cat) for cat in set(categorias)}
    # Cuenta los gastos por categoría.
    total_por_categoria = {cat: sum(gasto['monto'] for gasto in gastos.values() if gasto['categoria'] == cat) for cat in set(categorias)}
    # Suma los montos por categoría.
    
    # Crear la figura y los subplots
    # Comentario.
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    # Crea una figura con una cuadrícula de 2x2 subplots y un tamaño específico.
    fig.suptitle('📊 Análisis de Gastos', fontsize=20, weight='bold')
    # Establece un título para toda la figura.
    
    # Ajustar el espacio entre subplots
    # Comentario.
    plt.subplots_adjust(wspace=0.4, hspace=0.8) 
    # Ajusta el espacio horizontal y vertical entre los subplots.
    
    # Histograma de Cantidad de Gastos por Categoría
    # Comentario.
    axs[0, 0].bar(gastos_por_categoria.keys(), gastos_por_categoria.values(), color='skyblue')
    # Dibuja el histograma en el primer subplot (fila 0, columna 0).
    axs[0, 0].set_title('Cantidad de Gastos por Categoría', weight='bold')
    # Establece el título del subplot.
    axs[0, 0].set_xlabel('Categoría')
    # Establece la etiqueta del eje x.
    axs[0, 0].set_ylabel('Número de Gastos')
    # Establece la etiqueta del eje y.
    axs[0, 0].tick_params(axis='x', rotation=45)
    # Rota las etiquetas del eje x.
    
    # Gráfico de Barras de Monto Total por Categoría
    # Comentario.
    axs[0, 1].bar(total_por_categoria.keys(), total_por_categoria.values(), color='lightgreen')
    # Dibuja el gráfico de barras en el segundo subplot (fila 0, columna 1).
    axs[0, 1].set_title('Monto Total por Categoría', weight='bold')
    # Establece el título.
    axs[0, 1].set_xlabel('Categoría')
    # Establece la etiqueta del eje x.
    axs[0, 1].set_ylabel('Monto Total ($)')
    # Establece la etiqueta del eje y.
    axs[0, 1].tick_params(axis='x', rotation=45)
    # Rota las etiquetas del eje x.
    
    # Boxplot de la Distribución de Gastos
    # Comentario.
    montos_por_cat = {cat: [] for cat in set(categorias)}
    # Inicializa un diccionario con listas vacías.
    for gasto in gastos.values():
    # Itera sobre los gastos.
        montos_por_cat[gasto['categoria']].append(gasto['monto'])
    # Agrega el monto a su lista correspondiente.
    
    data_to_plot = [montos_por_cat[cat] for cat in montos_por_cat]
    # Prepara los datos para el boxplot.
    labels = list(montos_por_cat.keys())
    # Crea una lista de etiquetas.
    
    axs[1, 0].boxplot(data_to_plot, labels=labels)
    # Dibuja el boxplot en el tercer subplot (fila 1, columna 0).
    axs[1, 0].set_title('Distribución de Montos por Categoría (Boxplot)', weight='bold')
    # Establece el título.
    axs[1, 0].set_ylabel('Monto ($)')
    # Establece la etiqueta del eje y.
    axs[1, 0].tick_params(axis='x', rotation=45)
    # Rota las etiquetas del eje x.
    axs[1, 0].set_ylim(0, 1500)
    # Establece el límite del eje y.
    
    # Gráfico Circular (Pie Chart) de Cantidad de Gastos
    # Comentario.
    axs[1, 1].pie(gastos_por_categoria.values(), labels=gastos_por_categoria.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    # Dibuja el gráfico circular en el cuarto subplot (fila 1, columna 1).
    axs[1, 1].set_title('Proporción de Gastos por Categoría', weight='bold')
    # Establece el título.
    axs[1, 1].axis('equal')
    # Asegura que sea un círculo.
    
    # Mostrar la figura con los subplots
    # Comentario.
    plt.show()
    # Muestra todos los subplots en una única ventana.


# --- Bucle Principal del Programa ---
# Comentario.
gastos, id_contador = cargar_gastos(archivo)
# Llama a `cargar_gastos` al iniciar el programa para cargar los datos
# existentes y obtener el contador de ID.

while True:
# Inicia un bucle infinito que representa el menú principal del programa.
    limpiar_pantalla()
# Limpia la consola en cada iteración.
    mostrar_menu()
# Muestra el menú de opciones.
    
    opcion = input("➡️  Seleccione una opción: ")
# Pide al usuario que ingrese una opción.
    
    if opcion == '1':
    # Si la opción es '1'.
        gastos, id_contador = agregar_gasto(gastos, id_contador)
    # Llama a `agregar_gasto` y actualiza las variables `gastos` e `id_contador`.
    elif opcion == '2':
    # Si la opción es '2'.
        gastos = ver_gastos(gastos)
    # Llama a `ver_gastos`.
    elif opcion == '3':
    # Si la opción es '3'.
        gastos = actualizar_gasto(gastos)
    # Llama a `actualizar_gasto`.
    elif opcion == '4':
    # Si la opción es '4'.
        gastos = eliminar_gasto(gastos)
    # Llama a `eliminar_gasto`.
    elif opcion == '5':
    # Si la opción es '5'.
        gastos = guardar_gastos(gastos, archivo)
    # Llama a `guardar_gastos`.
    elif opcion == '6':
    # Si la opción es '6'.
        print("🔃 Cargando los datos desde el archivo...")
    # Muestra un mensaje informativo.
        gastos, id_contador = cargar_gastos(archivo)
    # Vuelve a cargar los datos del archivo, refrescando el estado del programa.
    elif opcion == '7':
    # Si la opción es '7'.
        gastos, id_contador = generar_gastos_falsos(gastos, id_contador)
    # Llama a `generar_gastos_falsos` y actualiza las variables.
        esperar_enter()
    # Pausa la ejecución.
    elif opcion == '8':
    # Si la opción es '8'.
        mostrar_todos_los_graficos(gastos)
    # Llama a la función que muestra todos los gráficos.
    elif opcion == '9':
    # Si la opción es '9'.
        mostrar_grafico_individual(gastos)
    # Llama a la función que muestra un solo gráfico a la vez.
    elif opcion == '0':
    # Si la opción es '0'.
        print("👋 Saliendo del programa. ¡Hasta luego!")
    # Muestra un mensaje de despedida.
        break
    # Termina el bucle `while True`, finalizando el programa.
    else:
    # Para cualquier otra entrada.
        print("❌ Opción no válida. Por favor, intente de nuevo.")
    # Muestra un mensaje de error.
        esperar_enter()
    # Pausa la ejecución.