def process_request(data):
    service = decode_service(data)
    data_fields = decode_data_fields(data)

    if service == 'uauth':
        if data_fields[0] == 'OKuauth':
            response_data = 'OKConnection established'
        else:
            db_service = 'dbcon'
            query = f"SELECT rut, type FROM usuario WHERE rut='{data_fields[0]}'"
            try:
                result = main_client(db_service, query)
                expected_type = data_fields[1]
                split_result = result.split(' ')
                user_rut = split_result[1]
                user_type = split_result[2]
                print("split_r: ", split_result)
                if user_type == expected_type:
                    response_data = f'OK User {user_rut} is authorized'
                else:
                    response_data = f'OK User {user_rut} {user_type} is not authorized for {expected_type}'

            except Exception as e:
                response_data = f'NK Internal error: {str(e)}'

    else:
        response_data = f'NK Invalid service name: {service}'

    return incode_response(service, response_data.strip())


if __name__ == "__main__":
    from service import main_service, decode_service, decode_data_fields, incode_response
    from client import main_client

    main_service('uauth', process_request)  # Use "dbcon" as the service
