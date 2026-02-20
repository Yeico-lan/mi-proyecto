from database import get_connection 

def verificar_usuario(username,password):
    """
    Verifica si el susuario existe en la base de datos.
    Retornna True si existe, False si no.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM usuarios
    WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))

    resultado = cursor.fetchone()

    connection.close()

    return resultado is not None