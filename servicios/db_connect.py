from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import json

"""
@   Conexión a la base de datos
*   Este archivo recibe un SQL como texto =>    "sql":"SELECT usuario FROM usuario WHERE nombre = :nombre"
*   Y los parametros =>                         "params": { "nombre": "Nico" }
*   Se asume que las query SQL estan correctas y los parámetros son válidos.
"""

load_dotenv()


def connect():
    """
    @   Función para crear una sesión
    *   Se conecta a la BDD usando SQLAlchemy. La BDD debe estar corriendo en el docker compose.
    """
    db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    Base = declarative_base()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def execute_sql_query(sql, params):
    """
    @   Función para ejecutar una query SQL
    *   Ejecuta la query con los parámetros y la retorna
    """
    session = connect()
    result = session.execute(text(sql), params)
    session.commit()
    session.close()
    return result


def parse_sql_result_to_json(sql_result):
    """
    @   Función para parsear el resultado SQL a JSON
    *   El resultado viene dado por filas, así que crea una lista de JSON con la forma { columna : valor }
    """
    column_names = sql_result.keys()
    result_list = []

    for row in sql_result:
        index = 0
        for column in column_names:
            value = str(row[index]).strip()
            row_dict = {
                column: value
            }
            result_list.append(row_dict)
            index = index + 1

    return result_list


def process_request(data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje
    *   Se asume que todos los mensajes tienen las llaves 'sql' y 'params'. Esto se debe validar previamente en
    *   el servicio que llame al servicio 'dbcon'
    """
    decoded_data = decode_response(data)
    print("decoded_data: ", decoded_data)
    length = decoded_data['length']
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service == 'dbcon':
        try:
            msg = json.loads(response)
            sql = msg['sql']
            params = msg['params']
            sql_result = execute_sql_query(sql, params)
            json_result = parse_sql_result_to_json(sql_result)
            response_data = {
                "data": json_result
            }
        except Exception as err:
            response_data = {
                "data": "Database Error: " + str(err)
            }
    else:
        response_data = {
            "data": "Invalid Service: " + service
        }

    return incode_response(service, response_data)


if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response

    main_service('dbcon', process_request)  # Use "dbcon" as the service
