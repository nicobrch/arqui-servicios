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
    if params is not None:
        result = session.execute(text(sql), params)
    else:
        result = session.execute(text(sql))
    session.commit()
    session.close()
    return result


def parse_sql_result_to_json(sql_result):
    """
    @   Función para parsear el resultado SQL a JSON
    *   El resultado viene dado por filas, así que crea una lista de JSON con la forma { columna : valor }
    """

    # Check if the result has rows (for SELECT queries)
    if sql_result.returns_rows:
        result_list = []
        column_names = sql_result.keys()
        row_index = 0

        for row in sql_result:
            row_list = []
            column_index = 0

            for column in column_names:
                value = str(row[column_index]).strip()
                row_dict = {
                    column: value
                }
                row_list.append(row_dict)
                column_index = column_index + 1

            result_list.append({str(row_index): row_list})
            row_index = row_index + 1

        return result_list
    else:
        # Handle non-SELECT queries (INSERT, UPDATE, DELETE)
        affected_rows = sql_result.rowcount
        return {"affected_rows": affected_rows}


def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje
    *   Se asume que todos los mensajes tienen las llaves 'sql' y 'params'. Esto se debe validar previamente en
    *   el servicio que llame al servicio 'dbcon'
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'dbcon':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        #   Si no hay query SQL, retorno con un error
        if 'sql' not in msg:
            return incode_response(service, {
                "data": "No SQL Query in data."
            })
        sql = msg['sql']

        #   Se pueden ejecutar queries con o sin parámetros, así que se define como None si no hay
        if 'params' not in msg:
            params = None
        else:
            params = msg['params']

        #   Se ejecuta la query usando las funciones
        sql_result = execute_sql_query(sql, params)
        json_result = parse_sql_result_to_json(sql_result)

        #   Se devuelven los resultados mediante le campo 'data'
        return incode_response(service, {
            "data": json_result
        })
    except Exception as err:
        return incode_response(service, {
            "data": "Database Error: " + str(err)
        })


if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response

    main_service('dbcon', process_request)  # Use "dbcon" as the service
