import socket


def menu():
    print("{ -- Servicio de Manejo de Usuarios -- }")
    print("[1] Crear un Usuario.")
    print("[2] Leer Usuarios.")
    print("[3] Actualizar un Usuario.")
    print("[4] Borrar un Usuario.")
    print("[0] Terminar Programa.")


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'usrmn'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            while True:
                menu()
                opcion = input()

                if opcion == '0':
                    break
                elif opcion == '1':
                    print("[ - Crear Usuario - ]")
                    usuario = input("Ingrese un usuario: ")
                    nombre = input("Ingrese un nombre: ")
                    cargo = input("Ingrese un cargo: ")
                    tipo = input("Ingrese un tipo: ")
                    password = input("Ingrese una contraseña: ")

                    #   Definimos la opción que elija como un diccionario
                    datos = {
                        "crear": {
                            "usuario": usuario,
                            "nombre": nombre,
                            "cargo": cargo,
                            "tipo": tipo,
                            "password": password
                        }
                    }
                    #   Enviamos el mensaje mediante el socket al servicio
                    send_message(sock, service, datos)

                    #   Recibimos la respuesta desde el socket
                    respuesta = receive_response(sock)
                    print("Respuesta: ", respuesta)

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":
    from client import send_message, receive_response

    main_client()
