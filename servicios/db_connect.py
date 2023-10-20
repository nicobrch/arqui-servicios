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
        # Assuming the data_fields contain a SQL query
        query = data_fields[0]
        try:
            result = execute_sql_query(query)
            response_data = f'OK{str(result)}'
        except Exception as e:
            response_data = str(e)
    else:
        response_data = 'NKInvalid service name'

    return incode_response(service, response_data)


if __name__ == "__main__":
    from service import main, decode_service, decode_data_fields, incode_response

    main("querydb", process_request)  # Use "querydb" as the service
