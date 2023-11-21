import socket
from client import input_field, service_request, print_select, print_ins_del_upd, get_session


def crear_comentario(sock, service):
    while True:
        print("[ - Hacer un Comentario - ]")
        print("[1] Buscar Asignaciones por Usuario.")
        print("[2] Buscar Asignaciones por Bloque.")
        print("[0] Volver.")
        opcion = input()

        if opcion == '0':
            print("Volviendo...")
            break
        elif opcion == '1':
            session = get_session()
            if 'id' not in session:
                print('Usuario no autenticado. Por favor inicie sesión.')
                break

            usuario = input_field("Ingrese usuario a buscar: ", max_length=20)
            datos = {
                "leer": "some",
                "usuario": usuario
            }
            #   Enviamos los datos al servicio
            status, user_data = service_request(sock, 'usrmn', datos)
            if 'id' not in user_data:
                print('No existe el usuario indicado.')
                break

            datos = {
                "leer": "some",
                "usuario_id": user_data['id']
            }
            #   Enviamos los datos al servicio
            status, assign_data = service_request(sock, 'asign', datos)
            print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
            print_select(status, assign_data)
            id_asignacion = input()
            texto = input("Ingrese comentario: ")

            datos = {
                "crear": {
                    "usuario_id": session['id'],
                    "asignacion_id": id_asignacion,
                    "texto": texto
                }
            }
            #   Enviamos los datos al servicio
            status, comment_data = service_request(sock, service, datos)
            print_ins_del_upd(status, comment_data)
        elif opcion == '2':
            session = get_session()
            if 'id' not in session:
                print('Usuario no autenticado. Por favor inicie sesión.')
                break

            dia = input_field("Ingrese dia de bloque a buscar: ", max_length=10)
            datos = {
                "leer": "some",
                "dia": dia
            }
            #   Enviamos los datos al servicio
            status, block_data = service_request(sock, 'block', datos)
            print("=== SELECCIONE UN ID DE BLOQUE ===")
            print_select(status, block_data)
            id_bloque = input()

            datos = {
                "leer": "some",
                "bloque_id": id_bloque
            }
            #   Enviamos los datos al servicio
            status, assign_data = service_request(sock, 'asign', datos)
            print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
            print_select(status, assign_data)
            id_asignacion = input()
            texto = input("Ingrese comentario: ")

            datos = {
                "crear": {
                    "usuario_id": session['id'],
                    "asignacion_id": id_asignacion,
                    "texto": texto
                }
            }
            #   Enviamos los datos al servicio
            status, comment_data = service_request(sock, service, datos)
            print_ins_del_upd(status, comment_data)


def leer_usuario(sock, service):
    print("[ - Leer Comentarios - ]")
    print("[1] Leer todos los usuarios.")
    print("[2] Buscar por Usuario.")
    print("[3] Buscar por Nombre.")
    print("[4] Buscar por Cargo.")
    print("[5] Buscar por Tipo.")
    opcion = input()

    if opcion == '1':
        datos = {
            "leer": "all"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '2':
        usuario = input_field("Ingrese usuario a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "usuario": usuario
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '3':
        nombre = input_field("Ingrese nombre a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "nombre": nombre
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '4':
        cargo = input_field("Ingrese cargo a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "cargo": cargo
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '5':
        tipo = input_field("Ingrese tipo a buscar: ", max_length=10)
        datos = {
            "leer": "some",
            "tipo": tipo
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    else:
        print("No existe esa opción.")


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'comnt'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            while True:
                print("{ -- Servicio de Comentarios -- }")
                print("[1] Hacer un Comentario.")
                print("[2] Leer Comentarios.")
                print("[0] Salir.")
                opcion = input()

                if opcion == '0':
                    print("Saliendo del servicio de manejo de usuarios...")
                    break

                elif opcion == '1':
                    crear_comentario(sock=sock, service=service)

                elif opcion == '2':
                    leer_usuario(sock=sock, service=service)

                else:
                    print("Opción erronea. Intente nuevamente.")

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    main_client()
