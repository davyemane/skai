import sys
import psycopg2
import MySQLdb
from pymongo import MongoClient
import json

def execute_postgresql(query, connection_params):
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        return str(e)

def execute_mysql(query, connection_params):
    try:
        conn = MySQLdb.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        return str(e)

def execute_mongodb(query, connection_params):
    try:
        client = MongoClient(**connection_params)
        db = client[connection_params['database']]
        result = eval(f"db.{query}")
        return result
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    db_type = input_data['db_type']
    query = input_data['query']
    connection_params = input_data['connection_params']

    if db_type == 'postgresql':
        print(execute_postgresql(query, connection_params))
    elif db_type == 'mysql':
        print(execute_mysql(query, connection_params))
    elif db_type == 'mongodb':
        print(execute_mongodb(query, connection_params))
    else:
        print(f"Unsupported database type: {db_type}")
