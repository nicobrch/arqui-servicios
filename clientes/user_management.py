import socket


def menu():
    print("{ -- Servicio de Manejo de Usuarios -- }")
    print("[1] Crear un Usuario.")
    print("[2] Leer Usuarios.")
    print("[3] Actualizar un Usuario.")
    print("[4] Borrar un Usuario.")
    print("[0] Terminar Programa.")


def valid_fields(user_input, max_length):
    if len(user_input) > max_length:
        return False
    if not user_input.isalnum():
        return False
    return True


def input_field(text_input, max_length):
    field = input(text_input)
    while not valid_fields(field, max_length):
        print(f"Error: Los datos no son correctos. Intente un largo máximo de {max_length} carácteres alfanuméricos.")
        field = input(text_input)
    return field


def service_request(sock, service, datos):
    #   Enviamos el mensaje mediante el socket al servicio
    send_message(sock, service, datos)
    #   Recibimos la respuesta desde el socket
    respuesta = receive_response(sock)
    return respuesta['status'], respuesta['data']


def crear_usuario(sock, service):
    print("[ - Crear Usuario - ]")
    usuario = input_field("Ingrese un usuario: ", max_length=20)
    nombre = input_field("Ingrese un usuario: ", max_length=20)
    cargo = input_field("Ingrese un usuario: ", max_length=20)
    tipo = input_field("Ingrese un usuario: ", max_length=10)
    password = input_field("Ingrese un usuario: ", max_length=50)
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
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    if status == 'OK':
        print(f"Se han insertado correctamente {data['affected_rows']} usuarios.")
    else:
        print(f"Ocurrió un error: {data}")


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
                    print("Saliendo del servicio de manejo de usuarios...")
                    break
                elif opcion == '1':
                    crear_usuario(sock=sock, service=service)

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    from client import send_message, receive_response

    main_client()
