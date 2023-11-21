import socket
from client import input_field, service_request, print_table

def print_select(status, data):
    if status == 'OK':
        if isinstance(data, list):
            print_table(data)
        else:
            print(data)
    else:
        print(f"Ocurrió un error: {data}")


def print_rud(status, data):
    if status == 'OK':
        print(data)
    else:
        print(f"Ocurrió un error: {data}")

def asignar_horario(sock, service):
    print("[ - Asignar horario - ]")
    usuario = input_field("Ingrese un usuario: ", max_length=20)
    hora_inicio = input_field("Ingrese una hora de inicio: ", max_length=4)
    hora_fin = input_field("Ingrese una hora de termino: ", max_length=4)
    dia = input_field("Ingrese un dia de la semana: ", max_length=20)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "asignar": {
            "usuario": usuario,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_rud(status, data)


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'asign'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            #   Acá deberíamos hacer un while true para que el usuario ingrese que desea realizar
            #   Definimos la opción que elija como un diccionario
            #asignar horario
            while True:
                print("[ - Asignar horario - ]")
                print("0: Salir")
                print("1: Asignar horario")
                opcion = input("Ingrese una opcion: ")

                if opcion == '0':
                    break
                elif opcion == '1':
                    asignar_horario(sock=sock, service=service)
                else:
                    print("Opcion no valida")
        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":

    main_client()
