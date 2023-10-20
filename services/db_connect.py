import psycopg2
from dotenv import load_dotenv
import os
import re

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


def parseQueryResponse(response):
    parsed = ""
    for tup in response:
        for item in tup:
            item = str(item)
            item = re.sub(r'[^a-zA-Z0-9]', '', item)
            parsed += item + " "
    return parsed


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
                result = parseQueryResponse(result)
                response_data = f'OK {str(result)}'
            except Exception as e:
                response_data = f'NK Internal error: {str(e)}'
    else:
        response_data = f'NK Invalid service name: {service}'

    return incode_response(service, response_data.strip())


if __name__ == "__main__":
    from service import main_service, decode_service, decode_data_fields, incode_response

    main_service('dbcon', process_request)  # Use "dbcon" as the service
