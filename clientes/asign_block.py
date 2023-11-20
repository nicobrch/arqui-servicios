import socket
from client import send_message, receive_response

def menu():
    print("Menu de opciones")
    print("0. Salir")
    print("1. Asignar horario")
    opcion = input("Ingrese una opcion: ")
    return opcion

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
                opcion = menu()
                if opcion == '0':
                    break
                elif opcion == '1':
                    print("[ - Asignar horario - ]")
                    usuario = input("Ingrese un usuario: ")
                    hora_inicio = input("Ingrese una hora de inicio: ")
                    hora_fin = input("Ingrese una hora de termino: ")
                    dia = input("Ingrese un dia de la semana: ")
                    #   Definimos la opción que elija como un diccionario
                    datos = {
                        "asignar": {
                            "usuario": usuario+"",
                            "hora_inicio": hora_inicio+"",
                            "hora_fin": hora_fin+"",
                            "dia": dia+""
                        }
                    }
                else:
                    print("Opcion no valida")

                send_message(sock, service, datos)
                respuesta = receive_response(sock)
                print("Respuesta: ", respuesta)
            
            """ 
            datos = {
                "asignar": {
                    "usuario": "nico",
                    "hora_inicio": "8",
                    "hora_fin": "18",
                    "dia": "Lunes"
                }
            }

            #   Enviamos el mensaje mediante el socket al servicio
            send_message(sock, service, datos)

            #   Recibimos la respuesta desde el socket
            respuesta = receive_response(sock)
            print("Respuesta: ", respuesta)
            """
        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":

    main_client()
