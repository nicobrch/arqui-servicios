

"""
asignar bloques de horario a usuarios
tabla asignacion

"""
import json


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
            #   Opción de crear usuarios
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
            #query para insertar en asignacion
            db_sql = {
                "sql": "INSERT INTO asignacion (id_usuario, id_bloque) VALUES ("
                       ":id_usuario, :id_bloque)",
                "params": {
                    "id_usuario": db_userrequest['data']['0']['id'],
                    "id_bloque": db_blockrequest['data']['0']['id'],
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
            "data": "asign block Error: " + str(err)
        })



if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response
    from user_management import process_db_request
    main_service('asign', process_request)  # Use "asign" as the service
