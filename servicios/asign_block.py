

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
    # extraer id de bloque
    blockId = get_bloque_ids(sock, fields['hora_inicio'], fields['hora_fin'], fields['dia'])
    blockId1 = blockId[0]['id']
    if blockId is None:
        return incode_response(service, {
            "data": "No existe el bloque."
        })
    #extraer id de asignacion
    #query para insertar en asignacion
    db_sql = {
        "sql": "INSERT INTO asignacion (usuario_id, bloque_id) VALUES (" 
               ":usuario_id, :bloque_id)",
        "params": {
            "usuario_id": userId,
            "bloque_id": blockId1
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




def leer(sock, service, msg):
    """
    @   Función para leer un o algunos bloques de horario
    *   Si el campo 'leer' es 'all', lee todos los bloques de horario sin filtros.
    *   Si el campo 'leer' es 'some', lee los bloques de horario de acuerdo su id, hora_inicio, hora_fin o dia.
    """
    if msg['leer'] == 'all':
        db_sql = {
            "sql": "SELECT * FROM asignacion"
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No hay bloques de horario."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif msg['leer'] == 'some':
        #   Opción de leer usuarios, habrá que verificar si se desea leer un usuario o muchos
        if 'id' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE id = :id",
                "params": {
                    "id": msg['id'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'usuario_id' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE usuario_id = :usuario_id",
                "params": {
                    "usuario_id": msg['usuario_id'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'bloque_id' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE bloque_id = :bloque_id",
                "params": {
                    "bloque_id": msg['bloque_id'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'hora_inicio' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE hora_inicio = :hora_inicio",
                "params": {
                    "hora_inicio": msg['hora_inicio'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'hora_fin' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE hora_fin = :hora_fin",
                "params": {
                    "hora_fin": msg['hora_fin'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif 'dia' in msg:
            db_sql = {
                "sql": "SELECT * FROM asignacion WHERE dia = :dia",
                "params": {
                    "dia": msg['dia'],
                }
            }
            db_request = process_db_request(sock, db_sql)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No hay bloques de horario."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        else:
            return incode_response(service, {
                "data": "No hay bloques de horario."
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
        elif 'leer' in msg:
            return leer(sock=sock, service=service, msg=msg)
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
