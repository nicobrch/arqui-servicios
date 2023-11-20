import socket
import json


def menu():
    print("{ -- Servicio de Manejo de Usuarios -- }")
    print("[1] Crear un Usuario.")
    print("[2] Leer Usuarios.")
    print("[3] Actualizar un Usuario.")
    print("[4] Borrar un Usuario.")
    print("[0] Salir.")


def crear_usuario(sock, service):
    print("[ - Crear Usuario - ]")
    usuario = input_field("Ingrese un usuario: ", max_length=20)
    nombre = input_field("Ingrese un nombre: ", max_length=20)
    cargo = input_field("Ingrese un cargo: ", max_length=20)
    tipo = input_field("Ingrese un tipo: ", max_length=10)
    password = input_field("Ingrese un password: ", max_length=50)
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


def leer_usuario(sock, service):
    print("[ - Leer Usuario - ]")
    print("[1] Leer todos los usuarios.")
    print("[2] Buscar por Usuario.")
    print("[3] Buscar por Nombre.")
    print("[4] Buscar por Cargo.")
    print("[5] Buscar por Tipo.")
    opcion = input()
    if opcion == '1':
        datos = {"leer": "all"}
        status, data = service_request(sock, service, datos)
        if status == 'OK':
            print(data)
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
                elif opcion == '2':
                    leer_usuario(sock=sock, service=service)

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    from client import input_field, service_request

    main_client()
