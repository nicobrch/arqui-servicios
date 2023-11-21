import os
import sys
from client import input_field, service_request, save_session, get_session

def print_menu():
    print("Seleccione un archivo para ejecutar:")
    print("1. Servicio de manejo de asignacion de bloques de horario")
    print("2. Servicio de manejo de comentarios")
    print("3. Servicio de manejo de bloques de horarios")
    print("4. Servicio de manejo de usuarios")

def print_menu2():
    print("Seleccione un archivo para ejecutar:")
    print("1. Servicio de manejo de asignacion de bloques de horario")
    print("2. Servicio de manejo de comentarios")

def execute_file(file_name):
    try:
        os.system(f"python {file_name}")
    except Exception as e:
        print(f"Error al ejecutar el archivo {file_name}: {e}")

if __name__ == "__main__":
    execute_file("user_login.py")
    session = get_session()
    if 'tipo' not in session or session['tipo'] == 'admin':
     print(session['tipo'])
     while True:
        print_menu()
        choice = input("Ingrese el número del archivo que desea ejecutar (0 para salir): ")

        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= 8:
            file_name = [
                "asign_block.py",
                "client_comment_management.py",
                "schedule_block.py",
                "user_management.py"
            ][int(choice) - 1]
# Si es necesario se podria de aqui mismo iniciar el servicio tambien
            execute_file(file_name)
        else:
            print("Opción no válida. Intente de nuevo.")
    if 'tipo' not in session or session['tipo'] == 'personal':
     print(session['tipo'])
     while True:
        print_menu2()
        choice = input("Ingrese el número del archivo que desea ejecutar (0 para salir): ")

        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= 8:
            file_name = [
                "asign_block.py",
                "client_comment_management.py",
            ][int(choice) - 1]
# Si es necesario se podria de aqui mismo iniciar el servicio tambien
            execute_file(file_name)
        else:
            print("Opción no válida. Intente de nuevo.")
