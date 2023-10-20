import socket


def send_message(sock, service, data):
    message = f"{len(service) + len(data):05d}{service}{data}"
    sock.sendall(message.encode())


def receive_response(sock):
    response_len = int(sock.recv(5).decode())
    response_service = sock.recv(5).decode()
    response_data = sock.recv(response_len - 5).decode()
    return response_data


def main_client(service, data):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5000)
    sock.connect(server_address)

    try:
        send_message(sock, service, data)
        response_data = receive_response(sock)
        print(f"Received: {response_data}")

    finally:
        print('Closing socket')
        sock.close()

    return response_data


if __name__ == "__main__":
    # Usage example:
    service = "usrlg"
    data = "1234 password1"
    main_client(service, data)
