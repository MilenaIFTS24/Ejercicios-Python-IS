# ControlGastos_GUI_final.py
# Gestor de Gastos con Tkinter — versión final con comentarios en cada línea.

# ------------------------------
# Imports
# ------------------------------
import os  # para manejo de rutas y extensiones
import sys  # para terminar el programa con sys.exit()
import json  # para leer/escribir archivos JSON
import csv  # para leer/escribir archivos CSV/TXT
import random  # para generar gastos simulados
from datetime import datetime  # para manejo de fechas y formateo
import uuid  # para generar IDs únicos por gasto
import tkinter as tk  # interfaz gráfica principal (Tk)
from tkinter import ttk, messagebox, filedialog, simpledialog  # widgets y diálogos de Tkinter
from tkcalendar import DateEntry, Calendar  # componente calendario para seleccionar fechas
import matplotlib.pyplot as plt  # para generar gráficos en ventanas separadas
from datetime import datetime, date, timedelta


# ------------------------------
# Configuración y variables globales
# ------------------------------
FORMATO_FECHA = "%d/%m/%Y"  # formato de fecha dd/mm/aaaa usado en todo el programa
gastos = []  # lista que almacenará los gastos como diccionarios
categorias = ["Comida", "Transporte", "Entretenimiento", "Hogar", "Salud", "Compras", "Otros"]  # categorías por defecto
archivo_actual = None  # ruta del archivo actualmente asociado (si el usuario importó o guardó)
root = None  # referencia a la ventana principal (se asigna luego)
tree = None  # referencia al Treeview de la tabla de gastos (se asigna luego)

# ------------------------------
# Utilidades: formateo y validaciones
# ------------------------------
def ahora_str():  # retorna la fecha de hoy en formato dd/mm/aaaa
    return datetime.now().strftime(FORMATO_FECHA)  # devuelve la fecha actual formateada

def validar_monto(monto_str):  # valida y convierte un string a float positivo con 2 decimales
    try:
        m = float(monto_str)  # intenta convertir a float
    except Exception:
        raise ValueError("Monto inválido. Ingresá un número válido.")  # lanza error si no se puede convertir
    if m < 0:  # chequea que sea no negativo
        raise ValueError("El monto debe ser mayor o igual a 0.")  # error si es negativo
    return round(m, 2)  # devuelve monto redondeado a 2 decimales

def parsear_fecha(fecha_texto):  # intenta parsear varias formas comunes de fecha y devuelve dd/mm/aaaa
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):  # formatos aceptados
        try:
            d = datetime.strptime(fecha_texto, fmt)  # intenta parsear
            return d.strftime(FORMATO_FECHA)  # devuelve en formato deseado
        except Exception:
            continue  # prueba el siguiente formato si falla
    raise ValueError("Formato de fecha inválido. Usá dd/mm/aaaa.")  # si todos fallan, lanza error

def generar_id():  # genera un id único para cada gasto
    return str(uuid.uuid4())  # usa UUID4 convertido a string

# ------------------------------
# Funciones I/O: importar y exportar gastos
# ------------------------------
def importar_gastos_ruta(ruta):  # importa desde ruta, soporta JSON/CSV/TXT
    ext = os.path.splitext(ruta)[1].lower()  # obtiene extensión del archivo
    lista = []  # lista temporal para almacenar registros importados
    if ext == ".json":  # si es JSON
        with open(ruta, "r", encoding="utf-8") as f:  # abre archivo en modo lectura
            data = json.load(f)  # carga JSON
        if isinstance(data, dict):  # si JSON es dict (posible id->registro)
            try:
                # intenta ordenar por clave numérica si aplica
                sorted_items = sorted(((int(k), v) for k, v in data.items()), key=lambda x: x[0])
                data = [v for _, v in sorted_items]  # convierte a lista ordenada
            except Exception:
                # si no son claves numéricas, lo tratamos como dict simple -> un elemento
                data = [data]
        if not isinstance(data, list):  # si no es lista ahora, error
            raise ValueError("JSON no contiene una lista de gastos.")
        for item in data:  # itera cada item esperado
            try:
                fecha = parsear_fecha(str(item.get("fecha", ahora_str())))  # parsea fecha
                categoria = str(item.get("categoria", "Otros"))  # obtiene categoría
                descripcion = str(item.get("descripcion", ""))  # obtiene descripción
                monto = float(item.get("monto", 0))  # obtiene monto
                lista.append({"id": generar_id(), "fecha": fecha, "categoria": categoria, "descripcion": descripcion, "monto": round(monto, 2)})  # agrega registro con id
            except Exception:
                continue  # si falla un registro, lo ignora
    elif ext in (".csv", ".txt"):  # si es CSV o TXT (esperamos columnas)
        with open(ruta, "r", encoding="utf-8", newline="") as f:  # abre archivo
            reader = csv.DictReader(f)  # usa DictReader para leer por nombre de columnas
            for row in reader:  # itera cada fila
                try:
                    fecha = parsear_fecha(row.get("fecha", ahora_str()))  # parsea fecha
                    categoria = row.get("categoria", "Otros")  # categoría
                    descripcion = row.get("descripcion", "")  # descripcion
                    monto = float(row.get("monto", 0))  # monto
                    lista.append({"id": generar_id(), "fecha": fecha, "categoria": categoria, "descripcion": descripcion, "monto": round(monto, 2)})  # agrega
                except Exception:
                    continue  # ignora filas inválidas
    else:
        raise ValueError("Formato no soportado (usar .json .csv .txt).")  # extensión no soportada
    return lista  # devuelve lista de registros válidos

def importar_gastos_dialogo():  # abre diálogo para importar y agrega a la lista principal
    global gastos, archivo_actual, categorias  # declara variables globales que modificaremos
    ruta = filedialog.askopenfilename(title="Importar gastos (JSON/CSV/TXT)", filetypes=[("JSON/CSV/TXT","*.json *.csv *.txt"),("All files","*.*")])  # diálogo
    if not ruta:  # si usuario canceló
        return  # no hace nada
    try:
        nuevos = importar_gastos_ruta(ruta)  # intenta importar desde la ruta
        if not nuevos:  # si no se importó nada
            messagebox.showwarning("Importar", "No se encontraron registros válidos en el archivo.")  # aviso
            return  # sale
        gastos.extend(nuevos)  # agrega los nuevos registros a la lista principal
        # actualizar categorías con las nuevas encontradas
        for c in {g["categoria"] for g in nuevos}:
            if c not in categorias:
                categorias.append(c)
        archivo_actual = ruta  # actualiza archivo actual
        refrescar_tabla()  # refresca la tabla en la UI
        messagebox.showinfo("Importar", f"Se importaron {len(nuevos)} gastos desde:\n{ruta}")  # confirma
    except Exception as e:
        messagebox.showerror("Error al importar", str(e))  # muestra error si falla

def guardar_gastos_dialogo():  # diálogo para guardar: si hay archivo_actual pregunta, o permite crear nuevo
    global archivo_actual  # variable global
    if archivo_actual:  # si existe un archivo asociado
        resp = messagebox.askyesnocancel("Guardar", f"¿Deseás guardar en el archivo actual?\n{archivo_actual}")  # pregunta sí/no/cancel
        if resp is None:  # cancelar
            return  # salir
        if resp:  # elegir guardar en archivo actual
            ok, err = guardar_en_ruta(archivo_actual)  # intenta guardar
            if not ok:
                messagebox.showerror("Error al guardar", err)  # muestra error si falla
            else:
                messagebox.showinfo("Guardado", f"Gastos guardados en:\n{archivo_actual}")  # confirma
            return  # sale
    # si llega acá, usuario quiere guardar en nuevo archivo o no había archivo actual
    # abrir ventana modal para elegir formato antes de abrir el explorador
    win = tk.Toplevel(root)  # crea Toplevel modal
    win.title("Guardar como...")  # título
    win.transient(root)  # modal respecto a root
    win.grab_set()  # bloquea interacción con ventana principal
    ttk.Label(win, text="Elegí formato:").pack(padx=12, pady=8)  # etiqueta
    var = tk.StringVar(value="json")  # variable para combobox
    cb = ttk.Combobox(win, textvariable=var, values=["json", "csv", "txt"], state="readonly")  # combobox de formatos
    cb.pack(padx=12, pady=6)  # empaqueta
    def confirmar():  # al confirmar
        fmt = var.get()  # obtiene formato
        win.destroy()  # cierra ventana
        # establece el extension y los filetypes según la elección
        if fmt == "json":
            ext = ".json"
            filetypes = [("JSON", "*.json")]
        elif fmt == "csv":
            ext = ".csv"
            filetypes = [("CSV", "*.csv")]
        else:
            ext = ".txt"
            filetypes = [("TXT", "*.txt")]
        ruta = filedialog.asksaveasfilename(defaultextension=ext, filetypes=filetypes, title="Guardar gastos")  # abre explorador con el tipo correcto
        if ruta:
            ok, err = guardar_en_ruta(ruta)  # guarda
            if ok:
                messagebox.showinfo("Guardado", f"Gastos guardados en:\n{ruta}")  # confirma
                archivo_actual = ruta  # actualiza archivo actual
            else:
                messagebox.showerror("Error al guardar", err)  # error
    ttk.Button(win, text="Confirmar", command=confirmar).pack(pady=8)  # botón confirmar
    ttk.Button(win, text="Cancelar", command=win.destroy).pack(pady=(0,12))  # botón cancelar

def guardar_en_ruta(ruta):  # escribe gastos en la ruta con formato según extensión
    try:
        ext = os.path.splitext(ruta)[1].lower()  # obtiene extensión
        if ext == ".json":  # json
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(gastos, f, indent=4, ensure_ascii=False)  # volcar lista como JSON
        elif ext == ".csv":  # csv
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "fecha", "categoria", "descripcion", "monto"])  # incluye id
                writer.writeheader()  # escribe cabecera
                for g in gastos:
                    writer.writerow(g)  # escribe fila por fila
        elif ext == ".txt":  # txt -> guardamos cada gasto como línea JSON para robustez
            with open(ruta, "w", encoding="utf-8") as f:
                for g in gastos:
                    f.write(json.dumps(g, ensure_ascii=False) + "\n")  # una línea JSON por gasto
        else:
            # si la extensión no es reconocida, lanzar error
            raise ValueError("Extensión no soportada para guardar.")
        return True, None  # éxito
    except Exception as e:
        return False, str(e)  # devuelve error

# ------------------------------
# CRUD: crear, editar, eliminar, buscar dinámico y refrescar UI
# ------------------------------
def refrescar_tabla(filtro_texto=""):  # refresca la vista de la tabla filtrando por categoría/descripcion
    global tree  # referencia al Treeview
    # borra todas las filas actuales
    for item in tree.get_children():
        tree.delete(item)
    # inserta solo los registros que coinciden con el filtro si existe
    texto = filtro_texto.strip().lower()  # texto de filtro en lower
    for g in gastos:
        if not texto or (texto in g["categoria"].lower() or texto in g["descripcion"].lower()):
            # usa el id como iid del tree para poder encontrar registros de manera estable
            tree.insert("", tk.END, iid=g["id"], values=(g["fecha"], g["categoria"], g["descripcion"], f"${g['monto']:.2f}"))  # inserta fila

def crear_gasto_modal():  # abre formulario emergente para crear un gasto
    win = tk.Toplevel(root)  # ventana modal
    win.title("Crear gasto")  # título
    win.transient(root)  # modal
    win.grab_set()  # bloquea principal
    # campo fecha con DateEntry
    ttk.Label(win, text="Fecha:").grid(row=0, column=0, padx=6, pady=6, sticky="e")  # etiqueta
    date = DateEntry(win, date_pattern="dd/mm/yyyy")  # componente calendario inline
    date.grid(row=0, column=1, padx=6, pady=6, sticky="w")  # coloca en grid
    # combobox de categorías
    ttk.Label(win, text="Categoría:").grid(row=1, column=0, padx=6, pady=6, sticky="e")  # etiqueta categoria
    cat_var = tk.StringVar(value=categorias[0])  # variable vinculada
    cb = ttk.Combobox(win, textvariable=cat_var, values=categorias)  # combobox editable
    cb.grid(row=1, column=1, padx=6, pady=6, sticky="w")  # coloca combobox
    # descripción
    ttk.Label(win, text="Descripción:").grid(row=2, column=0, padx=6, pady=6, sticky="e")  # etiqueta descripcion
    desc_entry = ttk.Entry(win, width=40)  # campo entrada descripcion
    desc_entry.grid(row=2, column=1, padx=6, pady=6, sticky="w")  # coloca
    # monto
    ttk.Label(win, text="Monto:").grid(row=3, column=0, padx=6, pady=6, sticky="e")  # etiqueta monto
    monto_entry = ttk.Entry(win, width=20)  # campo monto
    monto_entry.grid(row=3, column=1, padx=6, pady=6, sticky="w")  # coloca
    # label para mostrar validaciones de error localmente
    error_lbl = ttk.Label(win, text="", foreground="red")  # etiqueta de error en rojo
    error_lbl.grid(row=4, column=0, columnspan=2, padx=6, pady=(0,6))  # coloca
    # función que valida e inserta el gasto
    def guardar():
        try:
            fecha = date.get_date().strftime(FORMATO_FECHA)  # obtiene fecha en formato
            categoria_sel = cat_var.get().strip() or "Otros"  # obtiene categoria
            descripcion = desc_entry.get().strip() or ""  # descripcion
            monto = validar_monto(monto_entry.get().strip())  # valida monto
        except Exception as e:
            error_lbl.config(text=str(e))  # muestra error si falla validación
            return  # no cierra la ventana
        # si es nueva categoría, la agrega a la lista
        if categoria_sel not in categorias:
            categorias.append(categoria_sel)  # actualiza lista global
        # crea dict gasto con id
        nuevo = {"id": generar_id(), "fecha": fecha, "categoria": categoria_sel, "descripcion": descripcion, "monto": monto}
        gastos.append(nuevo)  # agrega a la lista principal
        refrescar_tabla()  # refresca UI
        win.destroy()  # cierra modal
    # botones guardar y cancelar
    ttk.Button(win, text="Guardar", command=guardar).grid(row=5, column=0, padx=6, pady=8)  # guardar
    ttk.Button(win, text="Cancelar", command=win.destroy).grid(row=5, column=1, padx=6, pady=8)  # cancelar

def seleccionar_gasto_por_iid(iid):  # helper: devuelve índice en lista 'gastos' a partir del iid (id)
    for idx, g in enumerate(gastos):
        if g["id"] == iid:
            return idx  # devuelve índice si coincide
    return None  # si no encuentra, devuelve None

def editar_gasto_modal():  # abre modal para editar el gasto seleccionado
    sel = tree.selection()  # ids seleccionados en tree
    if not sel:  # si no hay selección
        messagebox.showwarning("Editar", "Seleccioná un gasto primero.")  # aviso
        return  # sale
    iid = sel[0]  # toma el primer seleccionado
    idx = seleccionar_gasto_por_iid(iid)  # obtiene índice interno
    if idx is None:  # si no se encontró
        messagebox.showerror("Editar", "No se pudo localizar el gasto.")  # error
        return  # sale
    gasto = gastos[idx]  # obtiene gasto actual
    win = tk.Toplevel(root)  # modal
    win.title("Editar gasto")  # título
    win.transient(root)  # modal
    win.grab_set()  # bloquea ventana principal
    # fecha
    ttk.Label(win, text="Fecha:").grid(row=0, column=0, padx=6, pady=6, sticky="e")  # etiqueta
    date = DateEntry(win, date_pattern="dd/mm/yyyy")  # DateEntry
    try:
        date.set_date(datetime.strptime(gasto["fecha"], FORMATO_FECHA))  # intenta establecer la fecha actual
    except Exception:
        pass  # si falla, deja default
    date.grid(row=0, column=1, padx=6, pady=6, sticky="w")  # coloca
    # categoría
    ttk.Label(win, text="Categoría:").grid(row=1, column=0, padx=6, pady=6, sticky="e")  # etiqueta
    cat_var = tk.StringVar(value=gasto["categoria"])  # var con valor actual
    cb = ttk.Combobox(win, textvariable=cat_var, values=categorias)  # combobox
    cb.grid(row=1, column=1, padx=6, pady=6, sticky="w")  # coloca
    # descripción
    ttk.Label(win, text="Descripción:").grid(row=2, column=0, padx=6, pady=6, sticky="e")  # etiqueta
    desc_entry = ttk.Entry(win, width=40)  # entrada
    desc_entry.insert(0, gasto["descripcion"])  # inserta txt actual
    desc_entry.grid(row=2, column=1, padx=6, pady=6, sticky="w")  # coloca
    # monto
    ttk.Label(win, text="Monto:").grid(row=3, column=0, padx=6, pady=6, sticky="e")  # etiqueta
    monto_entry = ttk.Entry(win, width=20)  # entrada monto
    monto_entry.insert(0, str(gasto["monto"]))  # inserta monto actual
    monto_entry.grid(row=3, column=1, padx=6, pady=6, sticky="w")  # coloca
    # función aplicar cambios
    def aplicar():
        try:
            fecha_new = date.get_date().strftime(FORMATO_FECHA)  # nueva fecha
            categoria_new = cat_var.get().strip() or "Otros"  # nueva categoria
            descripcion_new = desc_entry.get().strip()  # nueva descripcion
            monto_new = validar_monto(monto_entry.get().strip())  # nuevo monto validado
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)  # muestra error
            return  # sale
        if categoria_new not in categorias:  # si categoria nueva se agrega
            categorias.append(categoria_new)  # agrega
        # actualiza gasto
        gasto["fecha"] = fecha_new
        gasto["categoria"] = categoria_new
        gasto["descripcion"] = descripcion_new
        gasto["monto"] = monto_new
        refrescar_tabla()  # refresca UI
        win.destroy()  # cierra modal
    # botones aplicar y cancelar
    ttk.Button(win, text="Aplicar cambios", command=aplicar).grid(row=4, column=0, padx=6, pady=8)  # aplicar
    ttk.Button(win, text="Cancelar", command=win.destroy).grid(row=4, column=1, padx=6, pady=8)  # cancelar

def eliminar_gasto_confirm():  # confirma y elimina el gasto seleccionado
    sel = tree.selection()  # obtiene selección
    if not sel:  # si no hay selección
        messagebox.showwarning("Eliminar", "Seleccioná un gasto primero.")  # aviso
        return  # sale
    iid = sel[0]  # primer seleccionado
    idx = seleccionar_gasto_por_iid(iid)  # índice en lista
    if idx is None:  # si no encontrado
        messagebox.showerror("Eliminar", "No se pudo localizar el gasto.")  # error
        return  # sale
    # confirmación
    if not messagebox.askyesno("Confirmar eliminación", "¿Eliminar el gasto seleccionado?"):
        return  # si cancela, sale
    gastos.pop(idx)  # elimina de la lista
    refrescar_tabla()  # refresca UI

# ------------------------------
# Generador de gastos simulados
# ------------------------------
def generar_gastos_simulados_dialog():  # pide cantidad y genera gastos aleatorios
    cantidad = simpledialog.askinteger("Generar gastos", "¿Cuántos gastos querés generar?", minvalue=1, maxvalue=1000)  # pide entero
    if not cantidad:  # si cancela o 0
        return  # sale
    hoy = datetime.now()  # fecha actual para variedad
    for _ in range(cantidad):  # genera la cantidad pedida
        dias = random.randint(0, 90)  # fecha aleatoria dentro de 90 días atrás
        fecha = (hoy - timedelta(days=dias)).strftime(FORMATO_FECHA)  # calcula fecha
        categoria = random.choice(categorias)  # elige categoria aleatoria
        descripcion = random.choice(["Compra", "Servicio", "Suscripción", "Regalo", "Varios"])  # descripcion aleatoria
        monto = round(random.uniform(20, 1500), 2)  # monto aleatorio
        gastos.append({"id": generar_id(), "fecha": fecha, "categoria": categoria, "descripcion": descripcion, "monto": monto})  # agrega gasto
    refrescar_tabla()  # refresca tabla al final
    messagebox.showinfo("Generar", f"Se generaron {cantidad} gastos de prueba.")  # informa

# ------------------------------
# Gráficos: boxplot, histograma, barras, pie y exportación
# ------------------------------
def crear_figura(tipo):  # crea y devuelve una figura matplotlib según tipo
    fig = plt.figure(figsize=(10, 6))  # crea figura con tamaño
    # si no hay datos, se dibuja un mensaje simple
    if not gastos:
        ax = fig.add_subplot(111)  # agrega eje
        ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")  # texto
        return fig  # retorna figura vacía
    # dependiendo del tipo, se dibuja en subplots
    if tipo == "boxplot":
        ax = fig.add_subplot(111)  # único subplot
        montos = [g["monto"] for g in gastos]  # lista montos
        ax.boxplot(montos, patch_artist=True, showmeans=True)  # boxplot con medias
        ax.set_title("Boxplot de montos")  # título
    elif tipo == "histograma":
        ax = fig.add_subplot(111)  # único subplot
        montos = [g["monto"] for g in gastos]  # lista montos
        ax.hist(montos, bins=12)  # histograma
        ax.set_title("Histograma de montos")  # título
    elif tipo == "barras":
        ax = fig.add_subplot(111)  # único subplot
        totals = {}  # diccionario categoria->suma
        for g in gastos:
            totals[g["categoria"]] = totals.get(g["categoria"], 0) + g["monto"]  # acumula por categoria
        cats = list(totals.keys())  # etiquetas
        vals = list(totals.values())  # valores
        ax.bar(cats, vals)  # barra
        ax.set_title("Monto total por categoría")  # título
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")  # rota etiquetas
    elif tipo == "pie":
        ax = fig.add_subplot(111)  # único subplot
        totals = {}  # acumula por categoria
        for g in gastos:
            totals[g["categoria"]] = totals.get(g["categoria"], 0) + g["monto"]  # suma
        labels = list(totals.keys())  # etiquetas
        sizes = list(totals.values())  # tamaños
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)  # pie chart
        ax.set_title("Proporción de gasto por categoría")  # título
    else:
        # tipo 'todos' -> 2x2 con los 4 gráficos
        axs = fig.subplots(2,2)  # subplots 2x2
        montos = [g["monto"] for g in gastos]  # montos
        # boxplot
        axs[0,0].boxplot(montos, patch_artist=True, showmeans=True)  # boxplot
        axs[0,0].set_title("Boxplot de montos")  # título
        # histograma
        axs[0,1].hist(montos, bins=12)  # histograma
        axs[0,1].set_title("Histograma de montos")  # título
        # barras
        totals = {}
        for g in gastos:
            totals[g["categoria"]] = totals.get(g["categoria"], 0) + g["monto"]
        axs[1,0].bar(list(totals.keys()), list(totals.values()))  # barra
        axs[1,0].set_title("Monto total por categoría")  # título
        plt.setp(axs[1,0].get_xticklabels(), rotation=45, ha="right")  # rotación etiquetas
        # pie
        axs[1,1].pie(list(totals.values()), labels=list(totals.keys()), autopct="%1.1f%%", startangle=140)  # pie
        axs[1,1].set_title("Proporción por categoría")  # título
    fig.tight_layout()  # ajusta espacios
    return fig  # devuelve la figura creada

def abrir_selector_graficos():  # abre menú para seleccionar gráfico individual o todos
    win = tk.Toplevel(root)  # ventana modal
    win.title("Seleccionar gráfico")  # título
    win.transient(root)  # modal
    win.grab_set()  # bloquea ventana principal
    ttk.Button(win, text="Boxplot", command=lambda:[win.destroy(), abrir_ventana_grafico("boxplot")]).pack(fill="x", padx=10, pady=6)  # botón
    ttk.Button(win, text="Histograma", command=lambda:[win.destroy(), abrir_ventana_grafico("histograma")]).pack(fill="x", padx=10, pady=6)  # botón
    ttk.Button(win, text="Barras", command=lambda:[win.destroy(), abrir_ventana_grafico("barras")]).pack(fill="x", padx=10, pady=6)  # botón
    ttk.Button(win, text="Pie", command=lambda:[win.destroy(), abrir_ventana_grafico("pie")]).pack(fill="x", padx=10, pady=6)  # botón
    ttk.Separator(win).pack(fill="x", pady=6)  # separador
    ttk.Button(win, text="Ver todos (2x2)", command=lambda:[win.destroy(), abrir_ventana_grafico("todos")]).pack(fill="x", padx=10, pady=6)  # ver todos
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=8)  # cerrar

def abrir_ventana_grafico(tipo):  # crea ventana con el gráfico embebido o en ventana matplotlib separada
    fig = crear_figura(tipo)  # crea figura según tipo
    # abrimos una ventana nueva de matplotlib (no embebida) para que sea separada y grande
    # esto abre la figura en la ventana nativa de matplotlib (backend)
    def export_png():  # exportar en PNG con diálogo que preselecciona png
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")], title="Exportar gráfico PNG")
        if ruta:
            fig.savefig(ruta)  # guarda figura
            messagebox.showinfo("Exportar", f"Gráfico guardado en:\n{ruta}")  # confirma
    def export_pdf():  # exportar en PDF con diálogo que preselecciona pdf
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")], title="Exportar gráfico PDF")
        if ruta:
            fig.savefig(ruta)  # guarda
            messagebox.showinfo("Exportar", f"Gráfico guardado en:\n{ruta}")  # confirma
    # mostrar ventana auxiliar con botones de exportación y then show figura matplotlib
    aux = tk.Toplevel(root)  # ventana auxiliar
    aux.title("Gráfico - opciones de exportación")  # título ventana auxiliar
    ttk.Button(aux, text="Exportar PNG", command=export_png).pack(side="left", padx=8, pady=8)  # botón png
    ttk.Button(aux, text="Exportar PDF", command=export_pdf).pack(side="left", padx=8, pady=8)  # botón pdf
    ttk.Button(aux, text="Cerrar", command=aux.destroy).pack(side="right", padx=8, pady=8)  # cerrar aux
    # mostrar la figura en una ventana separada del sistema (matplotlib)
    fig.show()  # abre la ventana nativa del backend de matplotlib

# ------------------------------
# Interfaz principal (construcción)
# ------------------------------
def construir_interfaz():  # función que construye y retorna la ventana root
    global root, tree  # usa las variables globales root y tree
    root = tk.Tk()  # crea la ventana principal
    root.title("Gestor de Gastos Personales")  # establece título de la ventana
    # intentamos maximizar la ventana en distintas plataformas
    try:
        root.state("zoomed")  # intento para Windows
    except Exception:
        try:
            root.attributes("-zoomed", True)  # intento para Linux/Mac
        except Exception:
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")  # fallback a pantalla completa
    # configurar cierre para que termine el proceso
    def on_close():  # función que se llama al cerrar la ventana principal
        if messagebox.askokcancel("Salir", "¿Querés salir de la aplicación?"):  # confirmación
            root.destroy()  # destruye la ventana
            sys.exit()  # termina el proceso de Python
    root.protocol("WM_DELETE_WINDOW", on_close)  # asocia la función al evento de cerrar ventana
    # layout: frame izquierdo (barra) y frame derecho (contenido)
    frame_left = ttk.Frame(root, width=260, padding=(8,8))  # frame lateral izquierdo
    frame_left.pack(side="left", fill="y")  # lo fija al lado izquierdo
    frame_main = ttk.Frame(root, padding=(8,8))  # frame principal a la derecha
    frame_main.pack(side="right", fill="both", expand=True)  # lo expande
    # logo genérico y saludo
    ttk.Label(frame_left, text="💰 Gestor de Gastos", font=("Segoe UI", 14, "bold")).pack(pady=(8,12))  # etiqueta título
    ttk.Label(frame_left, text="Bienvenido/a — elegí una opción", wraplength=220).pack(pady=(0,12))  # subtítulo
    # botones en la barra lateral (importar, guardar, crear, editar, eliminar, generar, gráficos, salir)
    ttk.Button(frame_left, text="📂 Importar gastos", command=importar_gastos_dialogo).pack(fill="x", pady=4)  # importar
    ttk.Button(frame_left, text="💾 Guardar / Exportar", command=guardar_gastos_dialogo).pack(fill="x", pady=4)  # guardar
    ttk.Separator(frame_left).pack(fill="x", pady=6)  # separador visual
    ttk.Button(frame_left, text="➕ Crear gasto manual", command=crear_gasto_modal).pack(fill="x", pady=4)  # crear gasto
    ttk.Button(frame_left, text="✏️ Editar gasto seleccionado", command=editar_gasto_modal).pack(fill="x", pady=4)  # editar
    ttk.Button(frame_left, text="🗑️ Eliminar gasto seleccionado", command=eliminar_gasto_confirm).pack(fill="x", pady=4)  # eliminar
    ttk.Separator(frame_left).pack(fill="x", pady=6)  # separador
    ttk.Button(frame_left, text="🎲 Generar gastos simulados", command=generar_gastos_simulados_dialog).pack(fill="x", pady=4)  # generar simulados
    ttk.Button(frame_left, text="📈 Ver gráficos", command=abrir_selector_graficos).pack(fill="x", pady=4)  # ver gráficos
    ttk.Separator(frame_left).pack(fill="x", pady=6)  # separador
    ttk.Button(frame_left, text="❌ Salir", command=lambda: (root.destroy(), sys.exit())).pack(fill="x", pady=8)  # salir y terminar proceso
    # área principal: búsqueda y tabla
    ttk.Label(frame_main, text="Lista de gastos", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,6))  # título sección
    # buscador dinámico
    search_var = tk.StringVar()  # variable vinculada al Entry
    search_entry = ttk.Entry(frame_main, textvariable=search_var)  # campo de búsqueda
    search_entry.pack(fill="x", pady=(0,8))  # empaqueta
    # cada vez que se suelta una tecla, se actualiza la vista (búsqueda dinámica)
    def on_key_release(event):  # callback
        refrescar_tabla(search_var.get())  # refresca con el texto actual
    search_entry.bind("<KeyRelease>", on_key_release)  # liga el evento
    # tabla de gastos (Treeview)
    cols = ("Fecha", "Categoría", "Descripción", "Monto")  # columnas visuales
    tree = ttk.Treeview(frame_main, columns=cols, show="headings", selectmode="browse")  # Treeview
    for c in cols:  # define encabezados
        tree.heading(c, text=c)  # pone encabezados
        tree.column(c, anchor="w")  # alinea a la izquierda
    tree.pack(fill="both", expand=True)  # empaqueta tabla
    # inicialmente la tabla está vacía; si el usuario importó al inicio, se rellenará más abajo
    return root  # devuelve la referencia a la ventana construida

# ------------------------------
# Inicio de la aplicación: importar opcional al iniciar
# ------------------------------
def iniciar_aplicacion():  # función que controla la secuencia de inicio
    app = construir_interfaz()  # construye la UI y obtiene root
    # al iniciar, abrimos diálogo para que el usuario elija un archivo para importar o cancele
    ruta = filedialog.askopenfilename(title="Importar archivo al iniciar (opcional)", filetypes=[("JSON/CSV/TXT","*.json *.csv *.txt"),("All files","*.*")])  # diálogo inicial
    if ruta:  # si el usuario eligió un archivo
        try:
            nuevos = importar_gastos_ruta(ruta)  # intenta importar
            if nuevos:
                # actualiza lista principal y categorías
                gastos.extend(nuevos)  # agrega los importados
                for c in {g["categoria"] for g in nuevos}:
                    if c not in categorias:
                        categorias.append(c)  # agrega categorías nuevas
                # guarda ruta como archivo_actual
                global archivo_actual
                archivo_actual = ruta
                messagebox.showinfo("Importar", f"Se importaron {len(nuevos)} gastos desde:\n{ruta}")  # confirma
            else:
                messagebox.showwarning("Importar", "No se importaron registros válidos.")  # adv si no hay registros
        except Exception as e:
            messagebox.showerror("Error al importar", str(e))  # muestra error si falla
    refrescar_tabla()  # refresca la tabla (aunque esté vacía)
    # inicia mainloop en try/except para manejar KeyboardInterrupt limpiamente
    try:
        app.mainloop()  # ejecuta bucle principal
    except KeyboardInterrupt:
        pass  # ignora Ctrl+C en consola
    except SystemExit:
        pass  # ignora sys.exit() para que el proceso termine limpiamente

# ------------------------------
# Ejecutar aplicación
# ------------------------------
if __name__ == "__main__":  # punto de entrada estándar
    iniciar_aplicacion()  # llama a la función que inicia todo
