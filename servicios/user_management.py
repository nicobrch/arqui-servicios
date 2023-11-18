import json

"""
@   Manejo de usuarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""


def process_db_request(sock, sql):
    """
    @   Conexión al servicio de BDD
    *   Esta función recibe una query SQL con la cuál se intenta conectar a la base de datos mediante el servicio DBCON.
    *   Por tanto, para poder ejecutar es necesario tener corriendo el servicio de DBCON.
    """
    try:
        #   Hacemos el request al servicio 'dbcon' igual que con cualquier otro servicio
        db_request = incode_response('dbcon', sql)
        print(f'Requesting data from database...')
        send_message(sock, db_request)
        print(f'Waiting for response...')
        expected_length = int(receive_message(sock, 5).decode('utf-8'))
        received_data = receive_message(sock, expected_length)
        print(f'Received data: {received_data}')

        #   Los datos se encuentran en bytes, es necesario codificar los datos
        db_data = json.loads(received_data[7:])
        format_db_data = incode_response('dbcon', db_data)
        decode_db_data = decode_response(format_db_data)

        #   Retornamos los datos codificados
        return decode_db_data['data']
    except Exception as err:
        return {
            "data": "Database Error: " + str(err)
        }


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
            #   Opción de leer usuarios, habrá que verificar si se desea leer un usuario o muchos
            db_sql = {
                "sql": "SELECT usuario, nombre, cargo, tipo FROM usuario"
            }
            db_request = process_db_request(sock, db_sql)
            return incode_response(service, db_request)
        elif 'crear' in msg:
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
    from service import main_service, decode_response, incode_response, send_message, receive_message

    main_service('usrmn', process_request)  # Use "usrmn" as the service
