import socket


def main_client():

    service = 'cment'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

       
            usuario_id = input("Ingrese el Usuario_ID: ")
            asignacion_id = input("Ingrese el Asignacion_ID: ")
            texto = input("Ingrese el texto del comentario: ")

            datos = {
                "create": {
                    "usuario_id": usuario_id,
                    "asignacion_id": asignacion_id,
                    "texto": texto
                   }
                }

            respuesta = receive_response(sock)
            print("Respuesta:", respuesta)
        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":
    from client import send_message, receive_response
    
    main_client()
