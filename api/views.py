from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DatabaseConnectionSerializer, DatabaseConnectionCreateSerializer
from .models import DatabaseConnection
import psycopg2
import MySQLdb
import docker
import json
from pymongo import MongoClient

@api_view(['POST'])
def connect_db(request):
    serializer = DatabaseConnectionCreateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        host = data['host']
        port = data['port']
        user = data['user']
        password = data['password']
        database = data['database']
        db_type = data['db_type']
        name = data['name']

        try:
            # Tester la connexion
            if db_type == 'postgresql':
                connection = psycopg2.connect(
                    host=host, port=port, user=user, password=password, database=database
                )
            elif db_type == 'mysql':
                connection = MySQLdb.connect(
                    host=host, port=port, user=user, passwd=password, db=database
                )
            elif db_type == 'mongodb':
                client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/{database}")
                connection = client[database]
                connection.list_collection_names()  # Tester la connexion MongoDB
            else:
                return Response({'status': 'error', 'message': 'Unsupported database type.'}, status=400)

            # Fermer la connexion si applicable
            if db_type in ['postgresql', 'mysql']:
                connection.close()

            # Enregistrer dans la base locale
            db_connection = DatabaseConnection.objects.create(
                name=name, host=host, port=port, user=user, database_name=database, db_type=db_type
            )
            output_serializer = DatabaseConnectionSerializer(db_connection)
            return Response({'status': 'success', 'data': output_serializer.data}, status=201)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
    else:
        return Response({'status': 'error', 'errors': serializer.errors}, status=400)


@api_view(['GET'])
def list_connections(request):
    connections = DatabaseConnection.objects.all()
    serializer = DatabaseConnectionSerializer(connections, many=True)
    return Response({'status': 'success', 'data': serializer.data}, status=200)




@api_view(['POST'])
def execute_query(request):
    try:
        # Récupérer l'ID de la connexion et la requête
        connection_id = request.data.get('connection_id')
        query = request.data.get('query')

        if not connection_id or not query:
            return Response({'status': 'error', 'message': 'connection_id and query are required.'}, status=400)

        # Récupérer les détails de la connexion dans la base locale
        try:
            connection = DatabaseConnection.objects.get(id=connection_id)
        except DatabaseConnection.DoesNotExist:
            return Response({'status': 'error', 'message': 'Connection not found.'}, status=404)

        # Préparer les paramètres pour le conteneur Docker
        connection_params = {
            'host': connection.host,
            'port': connection.port,
            'user': connection.user,
            'password': '',  # Ajoutez un mécanisme pour récupérer le mot de passe sécurisé
            'database': connection.database_name,
        }
        input_data = json.dumps({
            'query': query,
            'db_type': connection.db_type,
            'connection_params': connection_params,
        })

        # Exécuter la requête dans un conteneur Docker
        client = docker.from_env()
        result = client.containers.run(
            'query_executor',
            command=[input_data],
            remove=True,
            stdout=True,
            stderr=True
        )

        # Retourner les résultats
        return Response({'status': 'success', 'result': result.decode('utf-8')}, status=200)

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)