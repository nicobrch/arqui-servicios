import json
from service import main_service, decode_response, incode_response
from user_management import process_db_request

def process_request(sock, data):
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])
print("prueba2")
    if service != 'cment':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'create' in msg:
            print("prueba3")
            fields: dict = msg['create']
            if 'usuario_id' and 'asignacion_id' and 'texto' not in fields:
                return incode_response(service, {
                    "data": "Incomplete comment fields."
            })
        db_sql = {
            "sql": "INSERT INTO comentarios (usuario_id, asignacion_id, texto) VALUES ("
                   ":usuario_id, :asignacion_id, :texto)",
            "params": {
                "usuario_id": fields['usuario_id'],
                "asignacion_id": fields['asignacion_id'],
                "texto": fields['texto'],
            }
        }
        db_request = process_db_request(sock, db_sql)
        return incode_response(service, db_request)
    elif 'delete' in msg:
        fields: dict = msg['delete']
        if 'asignacion_id' not in fields:
            return incode_response(service, {
                "data": "Incomplete comment fields."
            })
        db_sql = {
            "sql": "DELETE FROM comentarios WHERE id = :asignacion_id",
            "params": {
                "asignacion_id": msg['asignacion_id']
            }
        }
        db_request = process_db_request(sock, db_sql)
        return incode_response(service, db_request)
    elif 'update' in msg:
        fields: dict = msg['update']
        if 'comentario_id' and 'usuario_id' and 'asignacion_id' and 'texto' not in msg:
            return incode_response(service, {
                "data": "Incomplete comment fields."
            })
        db_sql = {
            "sql": "UPDATE comentario SET usuario_id = :usuario_id, asignacion_id = :asignacion_id, texto = :texto WHERE id = :comentario_id",
            "params": {
                "comentario_id": msg['comentario_id'],
                "usuario_id": msg['usuario_id'],
                "asignacion_id": msg['asignacion_id'],
                "texto": msg['texto']
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
    Función main
    Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    print("prueba1")
    main_service('cment', process_request)  # Use "cment" as the service

