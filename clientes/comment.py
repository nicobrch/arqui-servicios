import socket
from client import (input_field, service_request, print_select, print_ins_del_upd, get_session, auth_session,
                    input_id_field)

session = get_session()


def crear_comentario_admin(sock, service):
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

            #   Definir usuario a buscar
            usuario = input_field("Ingrese usuario a buscar: ", max_length=20)
            datos = {
                "leer": "some",
                "usuario": usuario
            }
            #   Enviamos los datos al servicio
            status, user_data = service_request(sock, 'usrmn', datos)
            user = user_data[0]
            if 'id' not in user:
                print('No existe el usuario indicado.')
                break

            #   Buscar asignaciones del usuario
            datos = {
                "leer": "some",
                "usuario_id": user['id']
            }
            #   Enviamos los datos al servicio
            status, assign_data = service_request(sock, 'asign', datos)

            if len(assign_data) == 0:
                print("No existen asignaciones para el usuario. Cree una asignacion primero.")
                break

            print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
            print_select(status, assign_data)
            id_asignacion = input_id_field("Ingrese ID de asignacion: ", assign_data)
            texto = input_field("Ingrese comentario: ", max_length=100)

            #   Crear comentario
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

            datos = {
                "leer": "all"
            }
            #   Enviamos los datos al servicio
            status, block_data = service_request(sock, 'block', datos)

            if len(block_data) == 0:
                print("No existen bloques en este momento.")
                break

            print("=== SELECCIONE UN ID DE BLOQUE ===")
            print_select(status, block_data)
            id_bloque = input_id_field("Ingrese ID de asignacion: ", block_data)

            #   Buscar asignaciones correspondientes al bloque
            datos = {
                "leer": "some",
                "bloque_id": id_bloque
            }
            #   Enviamos los datos al servicio
            status, assign_data = service_request(sock, 'asign', datos)

            if len(assign_data) == 0:
                print("No existen asignaciones para el bloque. Cree una asignacion primero.")
                break

            print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
            print_select(status, assign_data)
            id_asignacion = input_id_field("Ingrese ID de asignacion: ", assign_data)
            texto = input_field("Ingrese comentario: ", max_length=100)

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


def crear_comentario_personal(sock, service):
    print("[ - Crear comentario por asignación - ]")

    datos = {
        "leer": "some",
        "usuario_id": session['id']
    }
    #   Obtenemos todas las asignaciones
    status, assign_data = service_request(sock, 'asign', datos)

    if len(assign_data) == 0:
        print("No existen asignaciones en este momento para ti.")
        return

    #   Dejamos que el usuario seleccione una asignacion por su id
    print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
    print_select(status, assign_data)
    id_asignacion = input_id_field("Ingrese ID de asignacion: ", assign_data)
    texto = input_field("Ingrese comentario: ", max_length=100)

    #   Leer comentarios según ID de asignación
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


def leer_comentarios_admin(sock, service):
    print("[ - Leer Comentarios por Asignación - ]")

    datos = {
        "leer": "all"
    }
    #   Obtenemos todas las asignaciones
    status, assign_data = service_request(sock, 'asign', datos)

    if len(assign_data) == 0:
        print("No existen asignaciones en este momento.")
        return

    #   Dejamos que el usuario seleccione una asignacion por su id
    print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
    print_select(status, assign_data)
    id_asignacion = input_id_field("Ingrese ID de asignacion: ", assign_data)

    #   Leer comentarios según ID de asignación
    datos = {
        "leer": "some",
        "asignacion_id": id_asignacion
    }
    #   Enviamos los datos al servicio
    status, comment_data = service_request(sock, service, datos)
    print_select(status, comment_data)


def leer_comentarios_personal(sock, service):
    print("[ - Leer Comentarios por Asignación - ]")
    datos = {
        "leer": "some",
        "usuario_id": session['id']
    }
    #   Obtenemos todas las asignaciones
    status, assign_data = service_request(sock, 'asign', datos)

    if len(assign_data) == 0:
        print("No existen asignaciones en este momento para ti.")
        return

    #   Dejamos que el usuario seleccione una asignacion por su id
    print("=== SELECCIONE UNA ID DE ASIGNACIÓN ===")
    print_select(status, assign_data)
    id_asignacion = input_id_field("Ingrese ID de asignacion: ", assign_data)

    #   Leer comentarios según ID de asignación
    datos = {
        "leer": "some",
        "asignacion_id": id_asignacion
    }
    #   Enviamos los datos al servicio
    status, comment_data = service_request(sock, service, datos)
    print_ins_del_upd(status, comment_data)


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

            if auth_session(session=session, tipo='admin'):
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
                        crear_comentario_admin(sock=sock, service=service)

                    elif opcion == '2':
                        leer_comentarios_admin(sock=sock, service=service)

                    else:
                        print("Opción erronea. Intente nuevamente.")
            elif auth_session(session=session, tipo='personal'):
                while True:
                    print("{ -- Servicio de Comentarios -- }")
                    print("[1] Ver mis comentarios por mis asignaciones.")
                    print("[2] Crear un comentario en mis asignaciones.")
                    print("[0] Salir.")
                    opcion = input()

                    if opcion == '0':
                        print("Saliendo del servicio de manejo de usuarios...")
                        break

                    elif opcion == '1':
                        crear_comentario_personal(sock=sock, service=service)

                    elif opcion == '2':
                        leer_comentarios_personal(sock=sock, service=service)

                    else:
                        print("Opción erronea. Intente nuevamente.")
            else:
                print("No existe una sesión actualmente.")

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    main_client()
