import json
from time import sleep
from service import main_service, decode_response, incode_response, process_db_request

"""
@   Manejo de comentarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'create' para insertar, 'delete' para borrar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""
def leer(sock, service, msg):
    """
    @   Función para leer un o algunos bloques de horario
    *   Si el campo 'leer' es 'all', lee todos los bloques de horario sin filtros.
    *   Si el campo 'leer' es 'some', lee los bloques de horario de acuerdo su id, hora_inicio, hora_fin o dia.
    """
    fields: dict = msg['leer']
    if 'asignacion_id' not in fields:
        db_sql = {
            "sql": "SELECT * FROM comentarios"
        }
        #   Opción de leer usuarios, habrá que verificar si se desea leer un usuario o muchos
    else:
        db_sql = {
            "sql": "SELECT asignacion_id FROM comentarios WHERE asignacion_id = :asignacion_id",
            "params": {
                "asignacion_id": fields['asignacion_id'],
            }
        }
    db_request = process_db_request(sock, db_sql)
    return incode_response(service, db_request)

def crear(sock, service, msg):
    """
    @   Función para insertar un comentario en la tabla comentarios
    *   Recibe un diccionario en "create", el cual debe incluir todos los campos de comentario requeridos.
    *   Ejemplo:    "create": { "usuario_id": "1", "asignacion_id": "2", "texto": "Hola" }
    """
    #   Opción de crear comentarios
    fields: dict = msg['crear']
    if 'usuario_id' and 'asignacion_id' and 'texto' not in fields:
        return incode_response(service, {
            "data": "Incomplete comment fields."
        })
    db_sql = {
        "sql": "INSERT INTO comentarios (usuario_id, asignacion_id, texto) VALUES ("
               ":usuario_id, :asignacion_id, :texto)",
        "params": {
            "usuario_id": fields['usuario_id'],
            "asignacion_id": fields['asignacion_id'],
            "texto": fields['texto'],
        }
    }
    db_request = process_db_request(sock, db_sql)
    print("sexoooooo",db_request)
    return incode_response(service, db_request)

def modificar(sock, service, msg):
    """
    @   Función para modificar un usuario
    *   Ejemplo:    "modificar" : { "usuario": "hola", "nombre": "hola", "cargo": "hola" }
    """
    fields: dict = msg['modificar']
    if 'asignacion_id' and 'usuario_id' and 'texto' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "UPDATE comentarios SET usuario_id = :usuario_id, texto = :texto WHERE asignacion_id = :asignacion_id",
        "params": {
            "asignacion_id": fields['asignacion_id'],
            "usuario_id": fields['usuario_id'],
            "texto": fields['texto'],
            "dia": fields['dia'],
        }
    }
    db_request = process_db_request(sock, db_sql)
    return incode_response(service, db_request)

def eliminar(sock, service, msg):
    """
    Deletes a block from the database based on the provided ID.

    Args:
        sock: The socket connection.
        service: The service name.
        msg: The message containing the block ID to be deleted.

    Returns:
        The response from the database operation.
    """
    fields: dict = msg['eliminar']
    if 'asignacion_id' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "DELETE FROM comentarios WHERE asignacion_id = :asignacion_id",
        "params": {
            "asignacion_id": fields['asignacion_id'],
        }
    }
    db_request = process_db_request(sock, db_sql)
    return incode_response(service, db_request)

def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'cment':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return leer(sock, service, msg)
        elif 'crear' in msg:
            return crear(sock=sock, service=service, msg=msg)
        elif 'modificar' in msg:
            return modificar(sock, service, msg)
        elif 'eliminar' in msg:
            return eliminar(sock, service, msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "schedule block Error: " + str(err)
        })

def main(sock, data):
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    try:
        return process_request(sock=sock, data=data)
    except Exception as e:
        print("Exception: ", e)
        sleep(20)
        main(sock, data)



if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    main_service('cment', main)  # Use "cment" as the service
