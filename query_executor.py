import sys
import json
import traceback

# Importations des bibliothèques de base de données
import psycopg2
import mysql.connector
from pymongo import MongoClient

def execute_postgresql(connection_params, query):
    """
    Exécute une requête sur une base de données PostgreSQL
    """
    try:
        # Ajouter des paramètres par défaut si nécessaire
        connection_params.setdefault('port', 5432)
        connection_params.setdefault('password', '')

        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        # Gérer différents types de requêtes
        if query.strip().upper().startswith('SELECT'):
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            cursor.execute(query)
            conn.commit()
            results = {'status': 'Query executed successfully'}

        cursor.close()
        conn.close()
        return results

    except Exception as e:
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def execute_mysql(connection_params, query):
    """
    Exécute une requête sur une base de données MySQL
    """
    try:
        # Ajuster les paramètres pour mysql-connector
        connection_params.setdefault('port', 3306)
        connection_params.setdefault('password', '')
        
        conn = mysql.connector.connect(**connection_params)
        cursor = conn.cursor(dictionary=True)
        
        # Gérer différents types de requêtes
        if query.strip().upper().startswith('SELECT'):
            cursor.execute(query)
            results = cursor.fetchall()
        else:
            cursor.execute(query)
            conn.commit()
            results = {'status': 'Query executed successfully'}

        cursor.close()
        conn.close()
        return results

    except Exception as e:
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def execute_mongodb(connection_params, query):
    """
    Exécute une requête sur une base de données MongoDB
    """
    try:
        # Construire l'URL de connexion MongoDB
        connection_string = f"mongodb://{connection_params['user']}:{connection_params.get('password', '')}@{connection_params['host']}:{connection_params['port']}"
        
        client = MongoClient(connection_string)
        db = client[connection_params['database']]
        
        # Exécuter la requête MongoDB
        collection_name, method = query.split('.', 1)
        collection = db[collection_name]
        
        # Évaluer dynamiquement la méthode MongoDB
        try:
            result = eval(f"collection.{method}")
        except Exception as eval_err:
            return {
                'error': f'Invalid MongoDB query: {eval_err}',
                'traceback': traceback.format_exc()
            }

        return list(result)

    except Exception as e:
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def main():
    """
    Point d'entrée principal pour l'exécution des requêtes
    """
    try:
        # Vérifier qu'un argument est passé
        if len(sys.argv) < 2:
            raise ValueError("Aucune donnée d'entrée fournie")

        # Parser les données JSON d'entrée
        try:
            input_data = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            raise ValueError("Format JSON invalide")

        # Extraire les paramètres nécessaires
        db_type = input_data.get('db_type')
        query = input_data.get('query')
        connection_params = input_data.get('connection_params', {})

        # Valider les paramètres d'entrée
        if not all([db_type, query, connection_params]):
            raise ValueError("Paramètres incomplets : db_type, query et connection_params sont requis")

        # Dispatcher vers la fonction appropriée
        if db_type == 'postgresql':
            result = execute_postgresql(connection_params, query)
        elif db_type == 'mysql':
            result = execute_mysql(connection_params, query)
        elif db_type == 'mongodb':
            result = execute_mongodb(connection_params, query)
        else:
            raise ValueError(f"Type de base de données non supporté : {db_type}")

        # Afficher le résultat en JSON
        print(json.dumps({
            'status': 'success',
            'result': result
        }, default=str))

    except Exception as e:
        # Gestion des erreurs génériques
        print(json.dumps({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()