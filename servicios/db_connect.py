from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import json

'''
@   Conexión a la base de datos
*   Este archivo recibe un SQL como texto:  sql = """INSERT INTO book(id, title) VALUES(:id, :title)"""
*   Y los parametros:   data = { "id": 1, "title": "The Hobbit" }
*   Ejemplo input:  { "sql": "SELECT...", "params" : { "nombre": "Nico" }, }
*   Se asume que antes de enviar una SQL ya se comprobaron los campos en el servicio determinado.
'''

load_dotenv()


def connect():
    db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    Base = declarative_base()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def execute_sql_query(sql, data):
    session = connect()
    result = session.execute(text(sql), **data)
    session.commit()
    session.close()
    return result


def parse_sql_response_to_json(sql_result):
    # Check if the result is falsy (empty list)
    if not sql_result:
        return json.dumps([], indent=2)
    # Fetch the column names from the result object
    columns = sql_result.keys()
    # Convert the result rows to a list of dictionaries
    rows = [dict(zip(columns, row)) for row in sql_result]
    # Convert the list of dictionaries to JSON
    json_result = json.dumps(rows, indent=2)

    return json_result


def process_request(data):
    decoded_data = decode_protocol(data)
    print("DECODED DATA: ", decoded_data)
    length = decoded_data['length']
    print("LENGTH: ", length)
    service = decoded_data['service']
    print("SERVICE: ", service)
    response = json.dumps(decoded_data['response'])
    print("RESPONSE: ", response)

    if service == 'dbcon':
        try:
            msg = json.loads(response)
            sql = msg['sql']
            params = msg['params']
            sql_result = execute_sql_query(sql, params)
            sql_result = parse_sql_response_to_json(sql_result)
            response_data = {
                "response": sql_result
            }
        except Exception as err:
            response_data = {
                "response": "Database Error: " + str(err)
            }
    else:
        response_data = {
            "response": "Invalid Service: " + service
        }

    return incode_response(service, response_data)


if __name__ == "__main__":
    from service import main_service, decode_protocol, decode_response, incode_response

    main_service('dbcon', process_request)  # Use "dbcon" as the service
