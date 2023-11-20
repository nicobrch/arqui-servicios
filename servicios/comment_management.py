import json
from time import sleep
from service import main_service, decode_response, incode_response, process_db_request

"""
@   Manejo de comentarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'create' para insertar, 'delete' para borrar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""

def create(sock, service, msg):
    """
    @   Función para insertar un comentario en la tabla comentarios
    *   Recibe un diccionario en "create", el cual debe incluir todos los campos de comentario requeridos.
    *   Ejemplo:    "create": { "usuario_id": "1", "asignacion_id": "2", "texto": "Hola" }
    """
    #   Opción de crear comentarios
    fields: dict = msg['create']
    if 'usuario_id' not in fields or 'asignacion_id' not in fields or 'texto' not in fields:
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
    return incode_response(service, db_request)

def delete(sock, service, msg):
    """
    @   Función para borrar un comentario de acuerdo a su asignacion_id.
    *   Ejemplo:    "delete": { "asignacion_id": "2" }
    """
    #   Opción de borrar comentarios
    fields: dict = msg['delete']
    if 'asignacion_id' not in fields:
        return incode_response(service, {
            "data": "Incomplete comment fields."
        })
    db_sql = {
        "sql": "DELETE FROM comentarios WHERE asignacion_id = :asignacion_id",
        "params": {
            "asignacion_id": fields['asignacion_id']
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
            return read(sock=sock, service=service, msg=msg)
        elif 'create' in msg:
            return create(sock=sock, service=service, msg=msg)
        elif 'delete' in msg:
            return delete(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "Comment Management Error: " + str(err)
        })

def main(sock, data):
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
