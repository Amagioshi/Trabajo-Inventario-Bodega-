# utilidades.py - Funciones para manejar la entrada del usuario de forma segura

# Función para solicitar un número entero al usuario con validación
# mensaje: texto que se muestra al usuario para pedir el dato
# minimo: valor mínimo permitido (opcional)
# maximo: valor máximo permitido (opcional)
# Devuelve un número entero válido
def solicitar_entero(mensaje: str, minimo: int = None, maximo: int = None) -> int:
    # Bucle infinito que se repite hasta que el usuario ingrese un valor válido
    while True:
        try:
            # Pedimos al usuario que ingrese un valor y lo convertimos a entero
            valor = int(input(mensaje))
            # Si se especificó un valor mínimo y el usuario ingresó un valor menor
            if minimo is not None and valor < minimo:
                # Mostramos un mensaje de error y repetimos el bucle
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            # Si se especificó un valor máximo y el usuario ingresó un valor mayor
            if maximo is not None and valor > maximo:
                # Mostramos un mensaje de error y repetimos el bucle
                print(f"El valor debe ser menor o igual a {maximo}.")
                continue
            # Si el valor es válido, lo devolvemos y salimos de la función
            return valor
        except ValueError:
            # Si el usuario no ingresó un número válido, mostramos un mensaje de error
            print("Por favor, ingrese un número entero válido.")


def solicitar_texto(mensaje: str, min_longitud: int = 1, max_longitud: int = 100, solo_letras: bool = False) -> str:
    while True:
        texto = input(mensaje).strip()
        if len(texto) < min_longitud:
            print(f"El texto debe tener al menos {min_longitud} caracteres.")
            continue
        if len(texto) > max_longitud:
            print(f"El texto no puede exceder los {max_longitud} caracteres.")
            continue
        if solo_letras and not texto.replace(" ", "").isalpha():
            print("El texto solo puede contener letras y espacios.")
            continue
        return texto
# Función para solicitar una opción de un conjunto predefinido
# mensaje: texto que se muestra al usuario para pedir la opción
# opciones_validas: lista de opciones que el usuario puede elegir
# Devuelve la opción seleccionada por el usuario
def solicitar_opcion(mensaje: str, opciones_validas: list) -> str:
    # Bucle infinito que se repite hasta que el usuario ingrese una opción válida
    while True:
        # Pedimos al usuario que ingrese una opción, eliminamos espacios y convertimos a minúsculas
        opcion = input(mensaje).strip().lower()
        # Si la opción ingresada está en la lista de opciones válidas
        if opcion in opciones_validas:
            # Devolvemos la opción y salimos de la función
            return opcion
        # Si la opción no es válida, mostramos un mensaje de error con las opciones permitidas
        print(f"Opción inválida. Las opciones válidas son: {', '.join(opciones_validas)}")