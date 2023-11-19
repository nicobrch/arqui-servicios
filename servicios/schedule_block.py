
import json
from service import main_service, decode_response, incode_response,process_db_request


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
        elif 'crear' in msg:
            #   Opción de crear usuarios
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
            db_request = process_db_request(sock, db_sql)
            return incode_response(service, db_request)
        elif 'modificar' in msg:
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
        elif 'eliminar' in msg:
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
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "schedule block Error: " + str(err)
        })



if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    main_service('block', process_request)  # Use "block" as the service
