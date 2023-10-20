import psycopg2
from dotenv import load_dotenv
import os

# Load env variables from .env
load_dotenv()

# Database connection parameters
db_params = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def execute_sql_query(sql):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def process_request(data):
    service = decode_service(data)
    data_fields = decode_data_fields(data)

    if service == 'dbcon':
        if data_fields[0] == 'OKdbcon':
            response_data = 'OKConnection established'
        else:
            query = ""
            for data in data_fields:
                query += data + ' '

            try:
                result = execute_sql_query(query)
                response_data = f'OK{str(result)}'
            except Exception as e:
                response_data = str(e)
    else:
        response_data = f'NKInvalid service name: {service}'

    return incode_response(service, response_data.strip())


if __name__ == "__main__":
    from service import main, decode_service, decode_data_fields, incode_response

    main('dbcon', process_request)  # Use "dbcon" as the service
