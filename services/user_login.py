import bcrypt
import re


def hash_password(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def extract_variables(input_string):
    match = re.search(r"OK\(\((\d+), '([^']+)', '([^']+)', '([^']+)', '([^']+)'.*\)\)", input_string)
    if match:
        rut, name, user_type, user_role, password = match.groups()
        return {
            "rut": int(rut),
            "name": name.strip(),
            "usr_type": user_type.strip(),
            "usr_role": user_role.strip(),
            "password": password
        }
    else:
        return None


def process_request(data):
    service = decode_service(data)
    data_fields = decode_data_fields(data)

    if service == 'usrlg':
        if data_fields[0] == 'OKusrlg':
            response_data = 'OKConnection established'
        else:
            db_service = 'dbcon'
            query = (f"SELECT rut, name, type, rol, created_at, updated_at FROM usuario WHERE rut='{data_fields[0]}' "
                     f"AND password='{data_fields[1]}'")
            try:
                result = main_client(db_service, query)
                response_data = f'OK{str(result)}'
            except Exception as e:
                response_data = f'NK{str(e)}'

    else:
        response_data = f'NKInvalid service name: {service}'

    return incode_response(service, response_data.strip())


if __name__ == "__main__":
    from service import main_service, decode_service, decode_data_fields, incode_response
    from client import main_client

    main_service('usrlg', process_request)  # Use "dbcon" as the service
