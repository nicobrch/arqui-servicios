import socket
import json

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
    data = json.dumps(data)
    msg_len = len(service) + len(data)
    message = f"{msg_len:05d}{service}{data}"
    encoded_msg = message.encode('utf-8')
    print("Sending: ", encoded_msg)
    sock.sendall(encoded_msg)


def receive_response(sock):
    """
    @   Recibir Mensaje
    *   Esta función escucha el socket y recibe los mensajes.
    *   Luego, decodifica los campos de acuerdo al patrón de mensaje del bus.
    *   Finalmente, retorna un JSON con 'status', 'service' y 'data'.
    """
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


def main_client(service: str, is_menu: bool, main_function):
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Se le debe indicar si es menú o no. Si es menú, se ejecutará en un loop infinito, sino, sólo una vez.
    *   Recibe una función main la cuál será programada en cada cliente con la lógica necesaria. Puedes ver como
    *   ejemplo el archivo 'example.py'
    """
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            if not is_menu:
                main_function(sock)
            else:
                while True:
                    main_function(sock)
        except KeyboardInterrupt:
            print(f'Terminating client {service}')
        finally:
            sock.close()
