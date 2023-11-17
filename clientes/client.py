import json
import socket

"""
@   Archivo principal de cliente
*   Todos los clientes deberán importar las funciones de este archivo.
"""


def send_message(sock, service: str, data: dict):
    """
    @   Enviar Mensaje
    *   Esta función recibe un string indicando el servicio y un diccionario para los datos (JSON).
    *   Luego, se envia siguiendo el formato del bus por el socket
    """
    try:
        data = json.dumps(data)
        msg_len = len(service) + len(data)
        message = f"{msg_len:05d}{service}{data}"
        encoded_msg = message.encode('utf-8')
        print("Sending: ", encoded_msg)
        sock.sendall(encoded_msg)
    except json.JSONDecodeError as json_error:
        print(f'Error decodificando JSON: {json_error}')
        raise RuntimeError('No se pudo decodificar el JSON.')
    except socket.error as sock_error:
        print(f'Error de socket: {sock_error}')
        raise RuntimeError('No se pudo recibir respuesta del socket.')
    except Exception as e:
        print(f'Error inesperado: {e}')
        raise RuntimeError('Ocurrio un error inesperado.')


def receive_response(sock):
    """
    @   Recibir Mensaje
    *   Esta función escucha el socket y recibe los mensajes.
    *   Luego, decodifica los campos de acuerdo al patrón de mensaje del bus.
    *   Finalmente, retorna un JSON con 'status', 'service' y 'data'.
    """
    try:
        response_len = int(sock.recv(5).decode())
        response_service = sock.recv(5).decode()
        response_data = sock.recv(response_len - 5).decode()
        response_status = response_data[:2]
        response_json = json.loads(response_data[2:])
        return {
            "status": response_status,
            "service": response_service,
            "data": response_json['data']
        }
    except (ValueError, json.JSONDecodeError) as json_error:
        print(f'Error decodifiando JSON: {json_error}')
        raise RuntimeError('No se pudo decodificar el JSON.')
    except socket.error as sock_error:
        print(f'Error de socket: {sock_error}')
        raise RuntimeError('No se pudo recibir respuesta del socket.')
    except Exception as e:
        print(f'Error inesperado: {e}')
        raise RuntimeError('Ocurrio un error inesperado.')
