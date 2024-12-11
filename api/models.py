from django.db import models

class DatabaseConnection(models.Model):
    TYPE_CHOICES = [
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('mongodb', 'MongoDB'),
    ]
    name = models.CharField(max_length=100, help_text="Nom ou description de la connexion")
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    user = models.CharField(max_length=100)
    database_name = models.CharField(max_length=100, help_text="Nom de la base distante")
    db_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.db_type})"
