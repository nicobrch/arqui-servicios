import socket
import json  

def valid_fields(user_input, max_length):
    if len(user_input) > max_length:
        return False
    if not user_input.isalnum():
        return False
    return True

def input_field(text_input, max_length):
    field = input(text_input)
    while not valid_fields(field, max_length):
        print(f"Error: Los datos no son correctos. Intente un largo máximo de {max_length} caracteres alfanuméricos.")
        field = input(text_input)
    return field

def service_request(sock, service, datos):
    # Convierte el diccionario a una cadena JSON antes de enviar
    data_json = json.dumps(datos)
    send_message(sock, service, data_json)
    respuesta = receive_response(sock)
    return respuesta['status'], respuesta['data']

def crear_comentario(sock, service):
    usuario_id = input_field("Ingrese el Usuario_ID: ", max_length=20)
    asignacion_id = input_field("Ingrese el Asignacion_ID: ", max_length=20)
    texto = input_field("Ingrese el texto del comentario: ", max_length=20)

    datos = {
        "create": {
            "usuario_id": usuario_id,
            "asignacion_id": asignacion_id,
            "texto": texto
        }
    }
    print("prueba")

    status, data = service_request(sock, service, datos)
    if status == 'OK':
        # Imprime la información en formato JSON
        print("Respuesta en formato JSON:", json.dumps(data, indent=2))
        print(f"Se han insertado correctamente {data['affected_rows']} comentarios.")
    else:
        print(f"Ocurrió un error: {data}")

def main_client():
    service = 'cment'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            crear_comentario(sock=sock, service=service)

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()

if __name__ == "__main__":
    from client import send_message, receive_response

    main_client()
