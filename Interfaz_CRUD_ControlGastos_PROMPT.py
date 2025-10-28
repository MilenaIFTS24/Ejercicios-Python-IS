"""Actúa como un experto desarrollador en Python y Tkinter.
Tengo un programa de control de gastos que actualmente funciona en consola.
Generá una versión con interfaz gráfica Tkinter minimalista, usando formularios integrados para ingresar y actualizar datos, y gráficos integrados en la interfaz usando matplotlib (FigureCanvasTkAgg).

Código base a modificar (para referencia completa):

[Código del ejercicio original]

Requerimientos específicos de la GUI:

Cada función principal del programa (Agregar, Ver, Actualizar, Eliminar, Guardar, Cargar, Generar datos falsos, Mostrar gráficos) debe tener un botón en la ventana principal.

Los formularios para agregar o actualizar gastos deben estar integrados en la ventana principal.

Las validaciones deben mostrarse como etiquetas de error junto al campo correspondiente.

Las confirmaciones (por ejemplo, al eliminar un gasto) deben aparecer como ventanas emergentes (messagebox).

Los gráficos (histograma, barras, boxplot, pie chart) se deben mostrar integrados en la GUI usando FigureCanvasTkAgg, manteniendo la lógica actual de los gráficos.

El estilo debe ser minimalista, usando los valores por defecto de Tkinter, pero organizado y legible.

El código debe mantener toda la lógica actual, incluyendo manejo de archivos JSON y generación de datos falsos.

La interfaz debe ser intuitiva y clara, con títulos, secciones y botones bien identificados.

Generá el código completo y listo para ejecutar con Tkinter, reemplazando la interacción por consola con la GUI según lo solicitado.
"""
##################################

"""
Refinamiento 1:
Vamos a mejorar el programa. Necesito lo siguiente:
La audiencia son estudiantes iniciales de programación con python.
Los gráficos deben actualizarse automáticamente cuando los datos se modifican.
Debe haber opción de exportar o importar gastos.
Debe haber opción de exportar cada gráfico.
Cada línea de código debe estar documentada.
"""

"""
Refinamiento 2:
Los gráficos deben mostrarse solo si se pide (a través de botones). Debo poder seleccionar cuál gráfico quiero ver, o alternativamente si quiero ver todos los gráficos juntos.
El programa debe importar los gastos desde el archivo gastos.json al iniciar (si es que existe el archivo), y debe guardar los gastos en el archivo cada vez que haya un cambio.
Debe haber un buscador para buscar un gasto o gastos específicos según categoría o descripción.
Debe haber un boton para mostrar todos los gastos.
Debe haber un botón para elegir crear un gasto de manera manual.
La pantalla de inicio debe tener un logo genérico y un saludo.
El título de la interfaz no debe decir: " - Educativo".
"""

"""
Refinamiento 3:
Al iniciar el programa, debe abrirse una ventana con las carpetas del sistema donde elegir el archivo que quiero importar. De elegir continuar sin importar, comenzar sin gastos cargados.
Al guardar los gastos, debe preguntar si quiero guardarlos en el archivo o crear un nuevo archivo. Si elijo crear un nuevo archivo, debe abrirse las carpetas del sistema para elegir donde quiero guardar el archivo y con qué nombre.
Debe haber un botón para salir del programa, que confirme si quiero salir y de aceptar que detenga la ejecución del programa.
Modificá el ingreso de la fecha para que se pueda elegir de un calendario en vez de hacerlo de forma manual.
"""

"""
Refinamiento 4:
Al exportar un gráfico, debe preguntar si quiero exportarlo en formato png o en formato pdf.
Al exportar o importar gastos, debe permitirme hacerlo en formato json, csv o txt.
La barra o menú de opciones principal debe estar del lado izquierdo.
En cualquier parte del programa que tenga una fecha, el formato debe ser dd/mm/aaaa.
Al seleccionar ver gráficos, debe darme la opción de elegir ver individualmente cada uno de los cuatro gráficos o verlos todos juntos.
La parte en la que se elige la categoría del gasto a crear debe ser una lista desplegable con las categorías disponibles.
"""

"""
Refinamiento 5:
Agrega el botón para generar un gasto simulado. Que me pregunte cuántos gastos quiero generar, y luego me los genere.
Que la pantalla al iniciar no muestre ningún formulario.
"""

"""
Refinamiento 6:
Al iniciarse el programa, se debe abrir en ventana maximizada.
Al seleccionar Ver gráficos, debe abrirse un menú con las opciones de ver gráficos individuales o todos los gráficos juntos.
Al seleccionar guardar gastos, debe darme a elegir con botones las opciones de guardado en diferentes formatos.
Al seleccionar un gasto, debe darme la opción de editarlo o eliminarlo.
Al seleccionar Guardar gastos, si elijo guardarlos en un archivo nuevo, los formatos a elegir deben ser dados como una lista desplegable o botones.
"""

"""
Refinamiento 7:
Al salir de la interfaz, debe detenerse la ejecución del programa automáticamente.
Quitá los botones de editar y eliminar de la parte inferior de la interfaz.
Quitá el formulario de creación de gastos que aparece inicialmente sobre la lista de gastos al comenzar el programa.
Al seleccionar exportar gráfico, debe darme opciones fijas de exportar en formato png o en formato pdf, no escritas en un cuadro de texto.
Al seleccionar el formato en el que quiero exportar los gastos, debe ponerse automáticamente ese formato en el Tipo del explorador de archivos.
Cuando busco un gasto, a medida que escribo debe ir reduciendo la lista a las coincidencias con el texto en el cuadro de búsqueda.
Los gráficos deben abrirse en una ventana aparte.
"""