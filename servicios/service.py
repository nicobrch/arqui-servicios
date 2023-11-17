import socket
import json


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


def decode_protocol(response):
    response = response.decode('utf-8')
    try:
        length = int(response[:5])
        service = response[5:10]
        response_data = json.loads(response[10:])
        if response[5:7] == 'OK' or response[5:7] == 'NK':
            service = response[7:12]
            response_data = json.loads(response[12:])
        return {
            "length": length,
            "service": service,
            "response": response_data
        }
    except ValueError:
        service = response[:5]
        response_data = json.loads(response[5:])
        if response[5:7] == 'OK' or response[5:7] == 'NK':
            service = response[7:12]
            response_data = json.loads(response[12:])
        return {
            "length": 0,
            "service": service,
            "response": response_data
        }


def decode_response(response):
    response = response.decode('utf-8')
    return json.loads(response[12:])


def incode_response(service, response):
    msg_len = len(service) + len(response)
    data_json = json.dumps(response)
    response_formatted = f'{msg_len:05d}{service}{data_json}'
    return response_formatted.encode('utf-8')


def is_sinit_response(response):
    response = response.decode('utf-8')
    if response[:5] == 'sinit':
        return True
    return False


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

            if is_sinit_response(data):
                continue

            print('Processing...')
            response = process_request(data)
            print(f'Sending response: {response}')
            send_message(sock, response)
