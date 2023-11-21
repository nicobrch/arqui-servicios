import os

def print_menu():
    print("Seleccione un archivo para ejecutar:")
    print("1. asign_block.py")
    print("2. client_comment_management.py")
    print("3. client.py")
    print("4. example.py")
    print("5. schedule_block.py")
    print("6. user_login.py")
    print("7. user_management.py")

def execute_file(file_name):
    try:
        #Aqui en vez de "python3" tienen que poner la forma en que ustedes ejecutan los archivos .py
        os.system(f"python3 {file_name}")
    except Exception as e:
        print(f"Error al ejecutar el archivo {file_name}: {e}")

if __name__ == "__main__":
    while True:
        print_menu()
        choice = input("Ingrese el número del archivo que desea ejecutar (0 para salir): ")

        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= 8:
            file_name = [
                "asign_block.py",
                "client_comment_management.py",
                "client.py",
                "example.py",
                "schedule_block.py",
                "user_login.py",
                "user_management.py"
            ][int(choice) - 1]

            execute_file(file_name)
        else:
            print("Opción no válida. Intente de nuevo.")
