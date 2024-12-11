from rest_framework import serializers
from .models import DatabaseConnection

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['id', 'name', 'host', 'port', 'user', 'database_name', 'db_type', 'created_at']

class DatabaseConnectionCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False, default="Default Connection")
    host = serializers.CharField(max_length=255)
    port = serializers.IntegerField(required=False)
    user = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    database = serializers.CharField(max_length=100)
    db_type = serializers.ChoiceField(choices=['postgresql', 'mysql', 'mongodb'])

    def validate(self, data):
        # Ajouter un port par défaut si non fourni
        if not data.get('port'):
            default_ports = {
                'postgresql': 5432,
                'mysql': 3306,
                'mongodb': 27017,
            }
            data['port'] = default_ports.get(data['db_type'])
        return data
