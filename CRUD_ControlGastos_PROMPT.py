"""
Hola gemini. Necesito desarrollar un programa en Python que muestre un menú interactivo en consola.
El menú debe permitir al usuario elegir Crear, Leer, Actualizar, Eliminar una lista , además de incluir
una opción para salir del programa.
Realizar el Menú usando un bucle White.
Utilizaremos ademas una lista para almacenar los datos.
Agregar las opciones de buscar, guardar en un archivo json, recuperar la
informacion del archivo guardado y salir del menú.
Usar diccionarios, y listas de ser necesario.
Documentar cada linea del programa.

REQUISITOS
1.- El menú debe estar dentro de un bucle while, permitiendo al usuario elegir distintas
opciones hasta que decida salir.
2.- Usar estructuras de control if, elif y else para gestionar las elecciones del menú.
3.- Limpiar la consola antes de mostrar el menú, utilizando os.system('cls') (solo para sistemas Windows).
4.- Colocar las pausas necesarias para mostrar la información / resultados.
5.- Usar la estructura FOR para recorrer el diccionario de datos.
6.- Cada vez que muestre el menu debe limpiarse la pantalla antes.

____
Me olvidé de aclarar el objetivo: es para un control de gastos personales, con los siguientes campos: Categoría, monto, fecha, descripción y un identificador único para usar en la búsqueda, actualización, etc.
____
El ejercicio debe estar hecho de manera sencilla, para principiantes en python.
____
Quitá el uso de la palabra reservada global. En vez de usar time.sleep, poné un input que le pida al usuario presionar enter para continuar.
____
Agrega la opción en el menú para que el usuario elija cargar el archivo gastos.json
____
Quita la linea opcional if __name__ == "__main__":
____
Asegurate de que cada línea del programa esté documentada.
____
Que en vez de ser una lista de diccionarios, sea un diccionario de diccionarios, donde la clave sea el id (el cual despues se utiliza para buscar, actualizar, etc.) y el valor sea el diccionario con los demás campos correspondientes al gasto.
"""