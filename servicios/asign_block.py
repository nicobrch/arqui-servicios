

"""
asignar bloques de horario a usuarios
tabla asignacion

"""
import json
from time import sleep
from service import main_service, decode_response, incode_response, process_db_request, get_bloque_ids, get_user_id


def asignar(sock, service, msg):
    """
    @   Función para asignar bloques de horario a usuarios
    *   Ejemplo:    "asignar" : { "usuario": "hola", "hora_inicio": "8", "hora_fin": "16", "dia": "lunes" }
    """
    fields = msg['asignar']
    if 'usuario' and 'hora_inicio' and 'hora_fin' and 'dia' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    
    # extraer id de usuario
    userId = get_user_id(sock, fields['usuario'])
    print("userId: ",userId)
    if userId is None:
        return incode_response(service, {
            "data": "No existe el usuario."
        })
    userId2 = userId[0]['id']
    print("userId2: ",userId2)
    # extraer id de bloque
    blockId = get_bloque_ids(sock, fields['hora_inicio'], fields['hora_fin'], fields['dia'])
    print("blockId1: ",blockId)
    if blockId is None:
        return incode_response(service, {
            "data": "No existe el bloque."
        })
    blockId = blockId[0]['id']
    print("blockId2: ",blockId)
    # extraer id de asignacion
    #query para insertar en asignacion
    db_sql = {
        "sql": "INSERT INTO asignacion (id_usuario, id_bloque) VALUES (" 
               ":id_usuario, :id_bloque)",
        "params": {
            "id_usuario": userId,
            "id_bloque": blockId
        }
    }
    db_request = process_db_request(sock, db_sql)
    if 'affected_rows' in db_request:
        return incode_response(service, {
            "data": f"se insertaron {db_request['affected_rows']} filas."
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
