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

def crear_bloque_horario(sock, service):
    print("[ - Crear bloque de horario - ]")
    hora_inicio = input_field("Ingrese una hora de inicio: ", max_length=4)
    hora_fin = input_field("Ingrese una hora de termino: ", max_length=4)
    dia = input_field("Ingrese un dia de la semana: ", max_length=20)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "crear": {
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_rud(status, data)

def leer_bloque_horario(sock, service):
    print("[ - Leer bloque de horario - ]")
    print("[1] Leer todos los bloques de horario.")
    print("[2] Buscar por id.")
    print("[3] Buscar por hora de inicio.")
    print("[4] Buscar por hora de termino.")
    print("[5] Buscar por dia de la semana.")
    opcion = input()

    if opcion == '1':
        datos = {
            "leer": "all"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '2':
        id = input_field("Ingrese id a buscar: ", max_length=4)
        datos = {
            "leer": "some",
            "id": id
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '3':
        hora_inicio = input_field("Ingrese hora de inicio a buscar: ", max_length=4)
        datos = {
            "leer": "some",
            "hora_inicio": hora_inicio
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '4':
        hora_fin = input_field("Ingrese hora de termino a buscar: ", max_length=4)
        datos = {
            "leer": "some",
            "hora_fin": hora_fin
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '5':
        dia = input_field("Ingrese dia a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "dia": dia
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    else:
        print("Opcion no valida")


def actualizar_bloque_horario(sock, service):
    print("[ - Actualizar bloque de horario - ]")
    print("[1] Actualizar hora de inicio.")
    print("[2] Actualizar hora de termino.")
    print("[3] Actualizar dia de la semana.")
    opcion = input()
    id = input_field("Ingrese id a buscar: ", max_length=3)

    if opcion == '1':
        hora_inicio = input_field("Ingrese hora de inicio a actualizar: ", max_length=4)
        datos = {
            "modificar": {
                "id": id,
                "hora_inicio": hora_inicio
            }
        }
        status, data = service_request(sock, service, datos)
        print_rud(status, data)
    elif opcion == '2':
        hora_fin = input_field("Ingrese hora de termino a actualizar: ", max_length=4)
        datos = {
            "modificar": {
                "id": id,
                "hora_fin": hora_fin
            }
        }
        status, data = service_request(sock, service, datos)
        print_rud(status, data)
    elif opcion == '3':
        dia = input_field("Ingrese dia a actualizar: ", max_length=20)
        datos = {
            "modificar": {
                "id": id,
                "dia": dia
            }
        }
        status, data = service_request(sock, service, datos)
        print_rud(status, data)
    else:   
        print("Opcion no valida")


def eliminar_bloque_horario(sock, service):
    print("[ - Eliminar bloque de horario - ]")
    id = input_field("Ingrese id a buscar: ", max_length=3)
    #   Definimos la opción que elija como un diccionario
    datos = {
            "borrar": id
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
    service = 'block'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            #   Acá deberíamos hacer un while true para que el usuario ingrese que desea realizar
            #   Definimos la opción que elija como un diccionario
            while True:
                print("{ -- Servicio de Manejo de bloques de horario -- }")
                print("[1] Crear bloque de horario.")
                print("[2] Leer bloque de horario.")
                print("[3] Actualizar bloque de horario.")
                print("[4] Eliminar bloque de horario.")
                print("[0] Salir.")

                opcion = input()

                if opcion == '0':
                    break
                elif opcion == '1':
                    crear_bloque_horario(sock=sock, service=service)
                elif opcion == '2':
                    leer_bloque_horario(sock=sock, service=service)
                elif opcion == '3':
                    actualizar_bloque_horario(sock=sock, service=service)
                elif opcion == '4':
                    eliminar_bloque_horario(sock=sock, service=service)
                else:
                    print("Opcion no valida")
                    continue
        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":

    main_client()
