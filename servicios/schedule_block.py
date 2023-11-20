
import json
from time import sleep
from service import main_service, decode_response, incode_response,process_db_request

def leer(sock, service, msg):
    """
    @   Función para leer un o algunos bloques de horario
    *   Si el campo 'leer' es 'all', lee todos los bloques de horario sin filtros.
    *   Si el campo 'leer' es 'some', lee los bloques de horario de acuerdo su id, hora_inicio, hora_fin o dia.
    """
    fields: dict = msg['leer']
    if 'id' not in fields:
        db_sql = {
            "sql": "SELECT * FROM bloque"
        }
        #   Opción de leer usuarios, habrá que verificar si se desea leer un usuario o muchos
    else:
        db_sql = {
            "sql": "SELECT id FROM bloque WHERE id = :id",
            "params": {
                "id": fields['id'],
            }
        }
    db_request = process_db_request(sock, db_sql)
    return incode_response(service, db_request)

def crear(sock, service, msg):
    """
    @   Función para crear un bloque de horarios
    *   Ejemplo:    "crear" : { "hora_inicio": "8", "hora_fin": "16", "dia": "lunes" }
    """
    fields: dict = msg['crear']
    if 'hora_inicio' and 'hora_fin' and 'dia' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "INSERT INTO bloque (hora_inicio, hora_fin, dia) VALUES ("
               ":hora_inicio, :hora_fin, :dia)",
        "params": {
            "hora_inicio": fields['hora_inicio'],
            "hora_fin": fields['hora_fin'],
            "dia": fields['dia'],
        }
    }

def modificar(sock, service, msg):
    """
    @   Función para modificar un usuario
    *   Ejemplo:    "modificar" : { "usuario": "hola", "nombre": "hola", "cargo": "hola" }
    """
    fields: dict = msg['modificar']
    if 'id' and 'hora_inicio' and 'hora_fin' and 'dia' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "UPDATE bloque SET hora_inicio = :hora_inicio, hora_fin = :hora_fin, dia = :dia WHERE id = :id",
        "params": {
            "id": fields['id'],
            "hora_inicio": fields['hora_inicio'],
            "hora_fin": fields['hora_fin'],
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
    if 'id' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "DELETE FROM bloque WHERE id = :id",
        "params": {
            "id": fields['id'],
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

    if service != 'block':
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
    main_service('block', main)  # Use "block" as the service
