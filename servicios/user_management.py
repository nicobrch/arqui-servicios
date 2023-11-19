import json

"""
@   Manejo de usuarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""


def create(sock, service, msg):
    """
    @   Función para insertar un usuario en la tabla usuario
    *   Recibe un diccionario en "crear", el cual debe incluir todos los campos de usuario requeridos.
    *   Ejemplo:    "crear" : { "usuario": "hola", "nombre": "hola", "cargo": "hola" }
    """
    #   Opción de crear usuarios
    fields: dict = msg['crear']
    if 'usuario' and 'nombre' and 'cargo' and 'tipo' and 'password' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "INSERT INTO usuario (usuario, nombre, cargo, tipo, password) VALUES ("
               ":usuario, :nombre, :cargo, :tipo, :password)",
        "params": {
            "usuario": fields['usuario'],
            "nombre": fields['nombre'],
            "cargo": fields['cargo'],
            "tipo": fields['tipo'],
            "password": fields['password']
        }
    }
    db_request = process_db_request(sock, db_sql)
    return incode_response(service, db_request)


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
        return incode_response(service, db_request)
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
            return incode_response(service, db_request)
        elif 'nombre' in msg:
            #   Leer usuario según campo "nombre".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE nombre = :nombre",
                "params": {
                    "nombre": msg['nombre']
                }
            }
            db_request = process_db_request(sock, db_sql)
            return incode_response(service, db_request)
        elif 'cargo' in msg:
            #   Leer usuario según campo "cargo".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE cargo = :cargo",
                "params": {
                    "cargo": msg['cargo']
                }
            }
            db_request = process_db_request(sock, db_sql)
            return incode_response(service, db_request)
        elif 'tipo' in msg:
            #   Leer usuario según campo "tipo".
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario WHERE tipo = :tipo",
                "params": {
                    "tipo": msg['tipo']
                }
            }
            db_request = process_db_request(sock, db_sql)
            return incode_response(service, db_request)
        else:
            #   No se incluyeron campos de lectura.
            return incode_response(service, {
                "data": "Incomplete SQL User Query. Provide some fields to search with."
            })


def update(sock, service, msg):
    """
    @   Función para actualizar un usuario.
    *   Recibe un diccionario en la llave 'update' de msg, que debe incluir el usuario a actualizar y el campo.
    *   Los campos que se pueden actualizar son nombre, cargo, tipo o password.
    *   Ejemplo:    "update": { "usuario": "hola", "password": "123" }
    """
    #   Opción de actualizar usuarios
    fields: dict = msg['update']
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
        return incode_response(service, db_request)
    elif 'cargo' in msg:
        #   Actualizar cargo de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET cargo = :cargo WHERE usuario = :usuario",
            "params": {
                "cargo": fields['cargo'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        return incode_response(service, db_request)
    elif 'tipo' in msg:
        #   Actualizar tipo de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET tipo = :tipo WHERE usuario = :usuario",
            "params": {
                "tipo": fields['tipo'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        return incode_response(service, db_request)
    elif 'password' in msg:
        #   Actualizar password de usuario.
        db_sql = {
            "sql": "UPDATE usuario SET password = :password WHERE usuario = :usuario",
            "params": {
                "password": fields['password'],
                "usuario": fields['usuario']
            }
        }
        db_request = process_db_request(sock, db_sql)
        return incode_response(service, db_request)
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
            "usuario": msg['usuario'],
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

    if service != 'usrmn':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            read(sock=sock, service=service, msg=msg)
        elif 'crear' in msg:
            create(sock=sock, service=service, msg=msg)
        elif 'actualizar' in msg:
            update(sock=sock, service=service, msg=msg)
        elif 'borrar' in msg:
            delete(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "User Management Error: " + str(err)
        })


if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response, process_db_request

    main_service('usrmn', process_request)  # Use "usrmn" as the service
