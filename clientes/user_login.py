import socket
import json


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'usrlg'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            while True:
                usuario = input_field("Ingrese un usuario: ", max_length=20)
                password = input_field("Ingrese su contraseña: ", max_length=50)
                #   Definimos la opción que elija como un diccionario
                datos = {
                    "login": {
                        "usuario": usuario,
                        "password": password
                    }
                }
                #   Enviamos los datos al servicio
                status, data = service_request(sock, service, datos)
                if status == 'OK':
                    if data == "Invalid credentials.":
                        print("Credenciales inválidas, intente nuevamente.")
                    else:
                        print(f"Inicio de sesión exitoso.")
                else:
                    print(f"Ocurrió un error: {data}")

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    from client import input_field, service_request

    main_client()
