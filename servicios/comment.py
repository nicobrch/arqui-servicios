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
            "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario"
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
        if 'usuario' in msg:
            #   Leer usuario según campo "usuario".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE usuario = :usuario",
                "params": {
                    "usuario": msg['usuario']
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
        elif 'nombre' in msg:
            #   Leer usuario según campo "nombre".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE nombre = :nombre",
                "params": {
                    "nombre": msg['nombre']
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
        elif 'cargo' in msg:
            #   Leer usuario según campo "cargo".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE cargo = :cargo",
                "params": {
                    "cargo": msg['cargo']
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
        elif 'tipo' in msg:
            #   Leer usuario según campo "tipo".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE tipo = :tipo",
                "params": {
                    "tipo": msg['tipo']
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


def update(sock, service, msg):
    """
    @   Función para actualizar un usuario.
    *   Recibe un diccionario en la llave 'update' de msg, que debe incluir el usuario a actualizar y el campo.
    *   Los campos que se pueden actualizar son nombre, cargo, tipo o password.
    *   Ejemplo:    "actualizar": { "usuario": "hola", "password": "123" }
    """
    #   Opción de actualizar usuarios
    fields: dict = msg['actualizar']
    if 'usuario' not in fields:
        return incode_response(service, {
            "data": "No user provided."
        })
    if 'nombre' in fields:
        #   Actualizar nombre de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET nombre = :nombre WHERE usuario = :usuario",
            "params": {
                "nombre": fields['nombre'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif 'cargo' in fields:
        #   Actualizar cargo de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET cargo = :cargo WHERE usuario = :usuario",
            "params": {
                "cargo": fields['cargo'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif 'tipo' in fields:
        #   Actualizar tipo de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET tipo = :tipo WHERE usuario = :usuario",
            "params": {
                "tipo": fields['tipo'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif 'password' in fields:
        #   Actualizar password de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET password = :password WHERE usuario = :usuario",
            "params": {
                "password": fields['password'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    else:
        #   No se incluyeron campos para actualizar.
        return incode_response(service, {
            "data": "Incomplete SQL User Query. Provide some fields to update with."
        })


def delete(sock, service, msg):
    """
    @   Función para borrar un usuario de acuerdo a su nombre de usuario.
    *   Ejemplo:    "borrar": "juanito"
    """
    #   Opción de crear usuarios
    db_sql = {
        "sql": "DELETE FROM usuario WHERE usuario = :usuario",
        "params": {
            "usuario": msg['borrar'],
        }
    }
    db_request = process_db_request(sock, db_sql)
    if 'affected_rows' in db_request:
        return incode_response(service, {
            "data": f"Se eliminaron {db_request['affected_rows']} usuarios."
        })
    else:
        return incode_response(service, {
            "data": db_request
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
        elif 'actualizar' in msg:
            return update(sock=sock, service=service, msg=msg)
        elif 'borrar' in msg:
            return delete(sock=sock, service=service, msg=msg)
        elif 'user_id' in msg:
            return get_user_id(sock=sock, service=service, msg=msg)
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
