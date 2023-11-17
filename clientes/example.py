def main_function(sock):
    """
    @   Cliente de ejemplo
    *   Ejecutaremos una query SQL en el servicio DBCON como prueba.
    *   Asegúrate siempre que los servicios que vayas a consultar esten en funcionamiento antes de ejecutar el cliente.
    """
    datos = {
        "sql": "SELECT usuario FROM usuario WHERE nombre = :nombre",
        "params": {
            "nombre": "Nico"
        }
    }
    send_message(sock, service, datos)
    respuesta = receive_response(sock)
    print("Respuesta: ", respuesta)


if __name__ == "__main__":
    from client import send_message, receive_response, main_client

    service = 'dbcon'
    main_client(service, False, main_function)
