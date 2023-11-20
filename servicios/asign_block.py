

"""
asignar bloques de horario a usuarios
tabla asignacion

"""
import json
from time import sleep
from service import main_service, decode_response, incode_response, process_db_request


def asignar(sock, service, msg):
    """
    @   Función para asignar bloques de horario a usuarios
    *   Ejemplo:    "asignar" : { "usuario": "hola", "hora_inicio": "8", "hora_fin": "16", "dia": "lunes" }
    """
    fields: dict = msg['asignar']
    if 'usuario' and 'hora_inicio' and 'hora_fin' and 'dia' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    # query para extraer id de usuario
    db_sql = {
        "sql": "SELECT id FROM usuario WHERE nombre = :usuario",
        "params": {
            "usuario": fields['usuario'],
        }
    }
    db_userrequest = process_db_request(sock, db_sql)
    print("db user request: ",db_userrequest.get('data')[0].get('id'))
    #query para extraer id de bloque
    db_sql = {
        "sql": "SELECT id FROM bloque WHERE hora_inicio = :hora_inicio AND hora_fin = :hora_fin AND dia = :dia",
        "params": {
            "hora_inicio": fields['hora_inicio'],
            "hora_fin": fields['hora_fin'],
            "dia": fields['dia'],
        }
    }
    db_blockrequest = process_db_request(sock, db_sql)
    print("db block request: ",db_blockrequest)
    #query para insertar en asignacion
    db_sql = {
        "sql": "INSERT INTO asignacion (id_usuario, id_bloque) VALUES ("
               ":id_usuario, :id_bloque)",
        "params": {
            "id_usuario": db_userrequest['data'][0]['id'],
            "id_bloque": db_blockrequest['data'][0]['id']
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

    if service != 'asign':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'asignar' in msg:
            return asignar(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "asign block Error: " + str(err)
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
    main_service('asign', main)  # Use "asign" as the service
