import socket


def send_message(sock, message):
    sock.sendall(message)


def receive_message(sock, expected_length):
    received_data = b''
    while len(received_data) < expected_length:
        data = sock.recv(expected_length - len(received_data))
        if not data:
            raise RuntimeError("Socket connection closed prematurely.")
        received_data += data
    return received_data


def decode_service(data):
    received_str = data.decode('utf-8')
    if received_str[5:7] == 'OK' or received_str[5:7] == 'NK':
        return received_str[7:12]

    if received_str[:5] == 'sinit':
        return received_str[5:10]

    return received_str[:5]


def decode_data_fields(data):
    received_str = data.decode('utf-8')
    return received_str[5:].split()


def incode_response(service, response_data):
    response = f'{len(service) + len(response_data):05d}{service}{response_data}'
    return response.encode('utf-8')


def main_service(service, process_request):
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)

        message = bytes(f'00010sinit{service}', 'utf-8')
        print(f'Sending message: {message}')
        send_message(sock, message)

        while True:
            print('Waiting for transaction...')
            expected_length = int(receive_message(sock, 5).decode('utf-8'))
            data = receive_message(sock, expected_length)
            print(f'Received data: {data}')

            print('Processing...')
            response = process_request(data)
            print(f'Sending response: {response}')
            send_message(sock, response)
