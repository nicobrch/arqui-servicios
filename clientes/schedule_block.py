import socket
from client import send_message, receive_response


def menu():
    print("{ -- Servicio de Manejo de Usuarios -- }")
    print("[1] Crear bloque de horario.")
    print("[2] Leer bloque de horario.")
    print("[3] Modificar bloque de horario.")
    print("[4] Eliminar bloque de horario.")
    print("[0] Salir.")

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
            """
            while True:
                menu()
                opcion = input()
                if opcion == '0':
                    break
                elif opcion == '1':
                    print("[ - Crear bloque de horario - ]")
                    hora_inicio = input("Ingrese una hora de inicio: ")
                    hora_fin = input("Ingrese una hora de termino: ")
                    dia = input("Ingrese un dia de la semana: ")
                    #   Definimos la opción que elija como un diccionario
                    #crear
                    datos = {
                        "crear": {
                            "hora_inicio": hora_inicio,
                            "hora_fin": hora_fin,
                            "dia": dia
                        }
                    }
                elif opcion == '2':
                    print("[ - Leer bloque de horario - ]")
                    id = input("Ingrese un id: ")
                    #   Definimos la opción que elija como un diccionario
                    #leer
                    datos = {
                        "leer": {
                            "id": id,
                        }
                    }
                elif opcion == '3':
                    print("[ - Modificar bloque de horario - ]")
                    id = input("Ingrese un id: ")
                    hora_inicio = input("Ingrese una hora de inicio: ")
                    hora_fin = input("Ingrese una hora de termino: ")
                    dia = input("Ingrese un dia de la semana: ")
                    #   Definimos la opción que elija como un diccionario
                    #modificar
                    datos = {
                        "modificar": {
                            "id": id,
                            "hora_inicio": hora_inicio,
                            "hora_fin": hora_fin,
                            "dia": dia
                        }
                    }
                elif opcion == '4':
                    print("[ - Eliminar bloque de horario - ]")
                    id = input("Ingrese un id: ")
                    #   Definimos la opción que elija como un diccionario
                    #eliminar
                    datos = {
                        "eliminar": {
                            "id": id,
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
                    "hora_inicio": "3",
                    "hora_fin": "7",
                    "dia": "lunes"
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

    main_client()
