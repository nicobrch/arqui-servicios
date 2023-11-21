import json
from time import sleep
from service import (main_service, decode_response, incode_response, process_db_request,
                     user_id_request)

"""
@   Manejo de usuarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""


def create(sock, service, msg):
    """
    @   Función para insertar un comentario a la tabla de comentarios
    *   Recibe un diccionario en "crear", el cual debe incluir todos los campos de usuario requeridos.
    *   Ejemplo:    "crear" : { "usuario_id": "1", "asignacion_id": "1", "texto": "hola" }
    """
    #   Opción de crear usuarios
    fields: dict = msg['crear']
    if 'usuario_id' and 'asignacion_id' and 'texto' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "INSERT INTO comentarios (usuario_id, asignacion_id, texto) VALUES ("
               ":usuario_id, :asignacion_id, :texto)",
        "params": {
            "usuario_id": fields['usuario_id'],
            "asignacion_id": fields['asignacion_id'],
            "texto": fields['texto']
        }
    }
    db_request = process_db_request(sock, db_sql)
    if 'affected_rows' in db_request:
        return incode_response(service, {
            "data": f"Se insertaron {db_request['affected_rows']} comentarios."
        })
    else:
        return incode_response(service, {
            "data": db_request
        })


def read(sock, service, msg):
    """
    @   Función para leer un o algunos usuarios
    *   Si el campo 'leer' es 'all', lee todos los usuarios sin filtros.
    *   Si el campo 'leer' es 'some', lee los usuarios de acuerdo su nombre de usuario, nombre, cargo o tipo.
    *   Ejemplo:    "leer": "some", "usuario": "hola"
    """
    if msg['leer'] == 'all':
        #   Opción de leer todos los usuarios
        db_sql = {
            "sql": "SELECT * FROM comentarios"
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No existen usuarios para la búsqueda solicitada."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif msg['leer'] == 'some':
        #   Opción de leer algunos usuarios, dependiendo de los campos.
        if 'usuario_id' in msg:
            #   Leer usuario según campo "usuario".
            db_sql = {
                "sql": "SELECT * FROM comentarios WHERE usuario_id = :usuario_id",
                "params": {
                    "usuario_id": msg['usuario_id']
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No existen comentarios para la búsqueda solicitada."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'asignacion_id' in msg:
            #   Leer usuario según campo "nombre".
            db_sql = {
                "sql": "SELECT * FROM comentarios WHERE asignacion_id = :asignacion_id",
                "params": {
                    "asignacion_id": msg['asignacion_id']
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No existen usuarios para la búsqueda solicitada."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        else:
            #   No se incluyeron campos de lectura.
            return incode_response(service, {
                "data": "Query SQL Incompleta. Por favor revisar los campos solicitados."
            })


def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'comnt':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)
        elif 'crear' in msg:
            return create(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "Comment Error: " + str(err)
        })


def main(sock, data):
    try:
        return process_request(sock=sock, data=data)
    except Exception as e:
        print("Exception: ", e)
        sleep(5)
        main(sock, data)


if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """

    main_service('comnt', main)  # Use "comnt" as the service
