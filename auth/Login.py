from database import get_connection # Importa la funcion que creamos antes de el archivo 'database'

def verificar_usuario(username,password): # Define una funcion que recibe un usuario y clave
    """
    Verifica si el susuario existe en la base de datos.
    Retornna True si existe, False si no.
    """

    connection = get_connection() # Llama la funcion anterior para abrir la puerta de la base de datos
    cursor = connection.cursor() # Crea un "cursor", que es el objeto que realmente ejecuta los comandos SQL

    query = """
    SELECT * FROM usuarios
    WHERE username = %s AND password = %s
    """

    # Ejecuta la pregunta reemplazando loss %s por el usuario y password reales de forma segura
    cursor.execute(query, (username, password))

    # Intentaa obtener una fila (un registro) que coincida con la busqueda 
    resultado = cursor.fetchone()


    connection.close() # Cierra la conexion para no desperdiciar recursos del servidor 

    # Si 'resultado' tiene algo, devuelve True; si esta vacio (None) devuelve False
    return resultado is not None