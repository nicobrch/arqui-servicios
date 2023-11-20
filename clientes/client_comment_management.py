import socket
from client import send_message, receive_response


def menu():
    print("{ -- Servicio de Manejo de Usuarios -- }")
    print("[1] Crear comentario.")


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'cment'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            #   Acá deberíamos hacer un while true para que el usuario ingrese que desea realizar
            #   Definimos la opción que elija como un diccionario

            while True:
                menu()
                opcion = input()
                if opcion == '0':
                    break
                elif opcion == '1':
                    print("[ - Crear comentario - ]")
                    usuario_id = input("Ingrese el Usuario_ID: ")
                    asignacion_id = input("Ingrese el Asignacion_ID: ")
                    texto = input("Ingrese el texto del comentario: ")
                    #   Definimos la opción que elija como un diccionario
                    #crear
                    datos = {
                        "crear": {
                            "usuario_id": usuario_id,
                            "asignacion_id": asignacion_id,
                            "texto": texto
                        }
                    }
                else:
                    print("Opcion no valida")
                    continue
                
                send_message(sock, service, datos)
                #   Recibimos la respuesta desde el socket
                respuesta = receive_response(sock)
                print("Respuesta: ", respuesta)

            """

            datos = {
                "crear": {
                    "usuario_id": "7",
                    "asignacion_id": "7",
                    "texto": "texto"
                }
            }
            #   Enviamos el mensaje mediante el socket al servicio
            send_message(sock, service, datos)
            #   Recibimos la respuesta desde el socket
            respuesta = receive_response(sock)
            print("Respuesta: ", respuesta)
        except ConnectionRefusedError:
            """
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":

    main_client()
